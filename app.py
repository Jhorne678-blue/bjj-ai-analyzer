from flask import Flask, request, jsonify, session, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sqlite3
import uuid
from datetime import datetime, timedelta
import json
from functools import wraps
import secrets

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov', 'mkv', 'webm'}

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Black Belt Access Codes
BLACK_BELT_CODES = {
    'BJJMASTER2024': {'uses_left': 10, 'expires': '2025-12-31'},
    'FRIENDCODE123': {'uses_left': 5, 'expires': '2025-06-30'},
    'UNLIMITED001': {'uses_left': -1, 'expires': '2026-01-01'}
}

def init_db():
    """Initialize the database with all necessary tables"""
    conn = sqlite3.connect('bjj_analyzer.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            plan TEXT DEFAULT 'free',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            subscription_expires TIMESTAMP,
            total_uploads INTEGER DEFAULT 0,
            monthly_uploads INTEGER DEFAULT 0,
            last_upload_month TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            filename TEXT NOT NULL,
            original_filename TEXT,
            upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            analysis_complete BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analysis_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id INTEGER,
            technique_name TEXT NOT NULL,
            category TEXT NOT NULL,
            confidence REAL NOT NULL,
            start_time REAL NOT NULL,
            end_time REAL NOT NULL,
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

def get_user_plan(user_id):
    conn = sqlite3.connect('bjj_analyzer.db')
    cursor = conn.cursor()
    cursor.execute('SELECT plan FROM users WHERE id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 'free'

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

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    plan = get_user_plan(user_id)
    
    conn = sqlite3.connect('bjj_analyzer.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM videos WHERE user_id = ?', (user_id,))
    total_videos = cursor.fetchone()[0]
    
    cursor.execute('SELECT monthly_uploads FROM users WHERE id = ?', (user_id,))
    monthly_uploads = cursor.fetchone()[0]
    
    conn.close()
    
    return render_template('dashboard.html', 
                         plan=plan, 
                         total_videos=total_videos,
                         monthly_uploads=monthly_uploads)

@app.route('/upload', methods=['POST'])
@login_required
def upload_video():
    user_id = session['user_id']
    
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400
    
    file = request.files['video']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file'}), 400
    
    filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    # Save to database
    conn = sqlite3.connect('bjj_analyzer.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO videos (user_id, filename, original_filename)
        VALUES (?, ?, ?)
    ''', (user_id, filename, file.filename))
    video_id = cursor.lastrowid
    
    # Simulate analysis results
    import random
    techniques = [
        {'name': 'armbar', 'category': 'submission', 'confidence': 0.87, 'start_time': 45.2, 'end_time': 52.1},
        {'name': 'triangle_c
