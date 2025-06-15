from flask import Flask, request, jsonify, session, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sqlite3
import uuid
from datetime import datetime, timedelta
import json
from analyzer import BJJAnalyzer
import yt_dlp
import tempfile
import threading
from functools import wraps
import secrets
import paypalrestsdk
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov', 'mkv', 'webm'}

# PayPal Configuration
paypalrestsdk.configure({
    "mode": os.environ.get('PAYPAL_MODE', 'sandbox'),
    "client_id": os.environ.get('PAYPAL_CLIENT_ID', 'your_paypal_client_id'),
    "client_secret": os.environ.get('PAYPAL_CLIENT_SECRET', 'your_paypal_client_secret')
})

# OAuth Configuration
oauth = OAuth(app)
facebook = oauth.register(
    name='facebook',
    client_id=os.environ.get('FACEBOOK_CLIENT_ID', 'your_facebook_client_id'),
    client_secret=os.environ.get('FACEBOOK_CLIENT_SECRET', 'your_facebook_client_secret'),
    server_metadata_url='https://graph.facebook.com/.well-known/openid_configuration',
    client_kwargs={'scope': 'openid email profile'}
)

# Initialize BJJ Analyzer
analyzer = BJJAnalyzer()

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('clips', exist_ok=True)

# Black Belt Access Codes
BLACK_BELT_CODES = {
    'BJJMASTER2024': {'uses_left': 10, 'expires': '2025-12-31'},
    'FRIENDCODE123': {'uses_left': 5, 'expires': '2025-06-30'},
    'UNLIMITED001': {'uses_left': -1, 'expires': '2026-01-01'}  # -1 = unlimited
}

def init_db():
    """Initialize the database with all necessary tables"""
    conn = sqlite3.connect('bjj_analyzer.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            plan TEXT DEFAULT 'free',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            subscription_expires TIMESTAMP,
            facebook_id TEXT,
            payment_method TEXT,
            black_belt_code TEXT,
            total_uploads INTEGER DEFAULT 0,
            monthly_uploads INTEGER DEFAULT 0,
            last_upload_month TEXT,
            preferences TEXT DEFAULT '{}'
        )
    ''')
    
    # Videos table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            filename TEXT NOT NULL,
            original_filename TEXT,
            youtube_url TEXT,
            upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            analysis_complete BOOLEAN DEFAULT FALSE,
            file_size INTEGER,
            duration REAL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Analysis results table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analysis_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id INTEGER,
            technique_name TEXT NOT NULL,
            category TEXT NOT NULL,
            confidence REAL NOT NULL,
            start_time REAL NOT NULL,
            end_time REAL NOT NULL,
            position TEXT,
            quality_score REAL,
            clip_path TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (video_id) REFERENCES videos (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long')
            return render_template('auth.html', mode='signup')
        
        password_hash = generate_password_hash(password)
        
        try:
            conn = sqlite3.connect('bjj_analyzer.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, last_upload_month)
                VALUES (?, ?, ?, ?)
            ''', (username, email, password_hash, datetime.now().strftime('%Y-%m')))
            conn.commit()
            
            user_id = cursor.lastrowid
            conn.close()
            
            session['user_id'] = user_id
            session['username'] = username
            flash('Account created successfully!')
            return redirect(url_for('dashboard'))
            
        except sqlite3.IntegrityError:
            flash('Username or email already exists')
            return render_template('auth.html', mode='signup')
    
    return render_template('auth.html', mode='signup')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('bjj_analyzer.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, password_hash FROM users WHERE username = ? OR email = ?', 
                      (username, username))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash('Logged in successfully!')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    
    return render_template('auth.html', mode='login')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/health')
def health():
    return jsonify({'status': 'running', 'message': 'BJJ AI Analyzer is ready!'})

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('DEBUG', 'False').lower() == 'true')
