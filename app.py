from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import os
import json
import secrets
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'bjj-ai-analyzer-secret-key-2024')

# Configuration
UPLOAD_FOLDER = 'uploads'
DATABASE = 'bjj_analyzer.db'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def init_database():
    """Initialize SQLite database"""
    conn = sqlite3.connect(DATABASE)
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
            total_uploads INTEGER DEFAULT 0,
            points INTEGER DEFAULT 0
        )
    ''')
    
    # Videos table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT,
            original_filename TEXT,
            upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            analysis_complete BOOLEAN DEFAULT FALSE,
            analysis_data TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    logger.info("Database initialized successfully")

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def login_required(f):
    """Decorator to require login"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    """Landing page"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>BJJ AI Analyzer</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-50">
        <div class="min-h-screen flex items-center justify-center">
            <div class="max-w-md w-full bg-white rounded-lg shadow-xl p-8 text-center">
                <h1 class="text-3xl font-bold text-gray-900 mb-4">🥋 BJJ AI Analyzer</h1>
                <p class="text-gray-600 mb-6">Professional Brazilian Jiu-Jitsu Video Analysis</p>
                <a href="/auth" class="bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700 transition-colors">
                    Get Started
                </a>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/auth')
def auth():
    """Authentication page"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login - BJJ AI Analyzer</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-50">
        <div class="min-h-screen flex items-center justify-center">
            <div class="max-w-md w-full bg-white rounded-lg shadow-xl p-8">
                <h2 class="text-2xl font-bold text-center mb-6">BJJ AI Analyzer</h2>
                
                <!-- Signup Form -->
                <form id="signup-form" class="space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Username</label>
                        <input type="text" name="username" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Email</label>
                        <input type="email" name="email" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Password</label>
                        <input type="password" name="password" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md">
                    </div>
                    <button type="submit" class="w-full bg-purple-600 text-white py-2 px-4 rounded-md hover:bg-purple-700">
                        Create Account
                    </button>
                </form>
                
                <div class="mt-4 text-center">
                    <a href="/dashboard" class="text-purple-600 hover:text-purple-800">Already have an account? Go to Dashboard</a>
                </div>
            </div>
        </div>
        
        <script>
        document.getElementById('signup-form').addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            
            try {
                const response = await fetch('/signup', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(Object.fromEntries(formData))
                });
                
                const result = await response.json();
                
                if (result.success) {
                    alert('Account created successfully!');
                    window.location.href = '/dashboard';
                } else {
                    alert(result.message);
                }
            } catch (error) {
                alert('Signup failed. Please try again.');
            }
        });
        </script>
    </body>
    </html>
    '''

@app.route('/signup', methods=['POST'])
def signup():
    """User registration"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not username or not email or not password:
            return jsonify({'success': False, 'message': 'All fields required'})
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute('SELECT id FROM users WHERE username = ? OR email = ?', (username, email))
        if cursor.fetchone():
            conn.close()
            return jsonify({'success': False, 'message': 'Username or email already exists'})
        
        # Create user
        password_hash = generate_password_hash(password)
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, plan)
            VALUES (?, ?, ?, 'free')
        ''', (username, email, password_hash))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Set session
        session['user_id'] = user_id
        session['username'] = username
        session['plan'] = 'free'
        
        return jsonify({'success': True, 'message': 'Account created successfully!'})
        
    except Exception as e:
        logger.error(f"Signup error: {str(e)}")
        return jsonify({'success': False, 'message': 'Registration failed'})

@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard - BJJ AI Analyzer</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-50">
        <div class="min-h-screen">
            <nav class="bg-white shadow-lg">
                <div class="max-w-7xl mx-auto px-4">
                    <div class="flex justify-between items-center h-16">
                        <div class="flex items-center">
                            <span class="text-xl font-bold text-gray-800">🥋 BJJ AI Analyzer</span>
                        </div>
                        <div class="text-sm text-gray-600">Welcome to your dashboard!</div>
                    </div>
                </div>
            </nav>
            
            <div class="max-w-7xl mx-auto px-4 py-8">
                <h1 class="text-3xl font-bold text-gray-900 mb-8">Dashboard</h1>
                
                <div class="grid md:grid-cols-3 gap-6 mb-8">
                    <div class="bg-white rounded-xl shadow-md p-6">
                        <div class="text-2xl font-bold text-purple-600">0</div>
                        <div class="text-sm text-gray-600">Videos Uploaded</div>
                    </div>
                    <div class="bg-white rounded-xl shadow-md p-6">
                        <div class="text-2xl font-bold text-green-600">0</div>
                        <div class="text-sm text-gray-600">Techniques Detected</div>
                    </div>
                    <div class="bg-white rounded-xl shadow-md p-6">
                        <div class="text-2xl font-bold text-yellow-600">Free</div>
                        <div class="text-sm text-gray-600">Current Plan</div>
                    </div>
                </div>
                
                <div class="bg-white rounded-xl shadow-md p-8">
                    <h2 class="text-xl font-semibold mb-4">Upload Video</h2>
                    <div class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
                        <div class="text-4xl mb-4">🎥</div>
                        <p class="text-lg text-gray-600 mb-2">Upload your BJJ training video</p>
                        <p class="text-sm text-gray-500">MP4, AVI, MOV supported (max 500MB)</p>
                        <button class="mt-4 bg-purple-600 text-white px-6 py-2 rounded-lg hover:bg-purple-700">
                            Select Video File
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''

# Initialize database on startup
try:
    init_database()
except Exception as e:
    logger.error(f"Database initialization failed: {str(e)}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)
