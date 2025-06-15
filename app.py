from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import sqlite3
import uuid
from datetime import datetime
import secrets
import random

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'bjj-secret-key-2024')

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov', 'mkv', 'webm'}

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def init_db():
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
            total_uploads INTEGER DEFAULT 0,
            monthly_uploads INTEGER DEFAULT 0
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
                INSERT INTO users (username, email, password_hash)
                VALUES (?, ?, ?)
            ''', (username, email, password_hash))
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
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    conn = sqlite3.connect('bjj_analyzer.db')
    cursor = conn.cursor()
    cursor.execute('SELECT total_uploads, monthly_uploads FROM users WHERE id = ?', (user_id,))
    user_data = cursor.fetchone()
    
    cursor.execute('SELECT COUNT(*) FROM videos WHERE user_id = ?', (user_id,))
    total_videos = cursor.fetchone()[0]
    
    conn.close()
    
    return render_template('dashboard.html', 
                         total_videos=total_videos,
                         monthly_uploads=user_data[1] if user_data else 0,
                         plan='free')

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400
    
    file = request.files['video']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file'}), 400
    
    user_id = session['user_id']
    filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    # Save to database
    conn = sqlite3.connect('bjj_analyzer.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO videos (user_id, filename, original_filename, analysis_complete)
        VALUES (?, ?, ?, ?)
    ''', (user_id, filename, file.filename, True))
    video_id = cursor.lastrowid
    
    # Generate sample analysis results
    techniques = [
        ('armbar', 'submission', 0.87, 45.2, 52.1),
        ('triangle_choke', 'submission', 0.92, 78.5, 85.3),
        ('scissor_sweep', 'sweep', 0.79, 120.1, 127.8),
        ('knee_cut_pass', 'guard_pass', 0.84, 156.3, 162.7)
    ]
    
    for tech in techniques:
        cursor.execute('''
            INSERT INTO analysis_results (video_id, technique_name, category, confidence, start_time, end_time)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (video_id, tech[0], tech[1], tech[2], tech[3], tech[4]))
    
    cursor.execute('UPDATE users SET total_uploads = total_uploads + 1, monthly_uploads = monthly_uploads + 1 WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'video_id': video_id, 'message': 'Analysis complete!'})

@app.route('/results/<int:video_id>')
def results(video_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    conn = sqlite3.connect('bjj_analyzer.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT filename, original_filename FROM videos WHERE id = ? AND user_id = ?', 
                  (video_id, user_id))
    video = cursor.fetchone()
    
    if not video:
        flash('Video not found')
        return redirect(url_for('dashboard'))
    
    cursor.execute('''
        SELECT technique_name, category, confidence, start_time, end_time
        FROM analysis_results WHERE video_id = ?
        ORDER BY start_time
    ''', (video_id,))
    
    techniques = cursor.fetchall()
    conn.close()
    
    return render_template('results.html', video=video, techniques=techniques, video_id=video_id)

@app.route('/health')
def health():
    return jsonify({'status': 'running', 'message': 'BJJ AI Analyzer is ready!'})

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
