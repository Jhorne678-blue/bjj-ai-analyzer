from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import os
import json
import secrets
import logging
from datetime import datetime, timedelta
from analyzer import BJJAnalyzer
from youtube_processor import YouTubeProcessor
import cv2

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'bjj-ai-analyzer-secret-key-2024')

# Configuration
UPLOAD_FOLDER = 'uploads'
CLIPS_FOLDER = 'clips'
DATABASE = 'bjj_analyzer.db'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CLIPS_FOLDER, exist_ok=True)
os.makedirs('static', exist_ok=True)
os.makedirs('templates', exist_ok=True)

# Initialize AI analyzer
bjj_ai = BJJAnalyzer()
youtube_processor = YouTubeProcessor()

def init_database():
    """Initialize SQLite database with all required tables"""
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
            monthly_uploads INTEGER DEFAULT 0,
            last_upload_month TEXT,
            friend_code_used TEXT,
            points INTEGER DEFAULT 0,
            facebook_id TEXT,
            subscription_expires TIMESTAMP
        )
    ''')
    
    # Videos table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT,
            original_filename TEXT,
            youtube_url TEXT,
            upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            analysis_complete BOOLEAN DEFAULT FALSE,
            duration REAL,
            file_size INTEGER,
            analysis_data TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Analysis results table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analysis_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id INTEGER NOT NULL,
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
    
    # Challenges table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS challenges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            points INTEGER DEFAULT 10,
            challenge_type TEXT DEFAULT 'daily',
            active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Challenge completions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS challenge_completions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            challenge_id INTEGER NOT NULL,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            video_id INTEGER,
            points_earned INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (challenge_id) REFERENCES challenges (id),
            FOREIGN KEY (video_id) REFERENCES videos (id)
        )
    ''')
    
    # Payments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            currency TEXT DEFAULT 'USD',
            plan TEXT NOT NULL,
            payment_method TEXT,
            transaction_id TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Friend codes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS friend_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            created_by INTEGER NOT NULL,
            uses_left INTEGER DEFAULT 5,
            expires_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (created_by) REFERENCES users (id)
        )
    ''')
    
    # AI learning table for continuous improvement
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ai_learning (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            technique_name TEXT NOT NULL,
            category TEXT NOT NULL,
            detection_count INTEGER DEFAULT 0,
            accuracy_sum REAL DEFAULT 0.0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            improvements TEXT DEFAULT '{}'
        )
    ''')
    
    # Insert default challenges if they don't exist
    cursor.execute('SELECT COUNT(*) FROM challenges')
    if cursor.fetchone()[0] == 0:
        default_challenges = [
            ('Daily Hip Escapes', 'Practice 20 hip escapes focusing on maximum distance', 'movement', 'beginner', 10, 'daily'),
            ('Daily Armbar Drill', 'Drill armbar setups from guard - 10 reps each side', 'submissions', 'intermediate', 15, 'daily'),
            ('Weekly Flow Session', 'Record 5-minute guard retention flow session', 'guard_retention', 'intermediate', 50, 'weekly'),
            ('Monthly Competition Prep', 'Upload 10-minute sparring session for analysis', 'sparring', 'advanced', 100, 'monthly'),
            ('Daily Takedown Practice', 'Practice double-leg takedown entries - 15 reps', 'takedowns', 'beginner', 12, 'daily'),
            ('Weekly Sweep Challenge', 'Demonstrate 5 different sweep techniques', 'sweeps', 'advanced', 75, 'weekly')
        ]
        
        cursor.executemany('''
            INSERT INTO challenges (title, description, category, difficulty, points, challenge_type)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', default_challenges)
    
    conn.commit()
    conn.close()
    logger.info("✅ Database initialized successfully")

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
    return render_template('index.html')

@app.route('/auth')
def auth():
    """Authentication page"""
    return render_template('auth.html')

@app.route('/signup', methods=['POST'])
def signup():
    """User registration"""
    try:
        data = request.get_json() or request.form
        username = data.get('username', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        friend_code = data.get('friend_code', '').strip()
        
        # Validation
        if not username or len(username) < 3:
            return jsonify({'success': False, 'message': 'Username must be at least 3 characters'})
        
        if not email or '@' not in email:
            return jsonify({'success': False, 'message': 'Please enter a valid email'})
        
        if not password or len(password) < 6:
            return jsonify({'success': False, 'message': 'Password must be at least 6 characters'})
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute('SELECT id FROM users WHERE username = ? OR email = ?', (username, email))
        if cursor.fetchone():
            conn.close()
            return jsonify({'success': False, 'message': 'Username or email already exists'})
        
        # Determine plan based on friend code
        plan = 'free'
        if friend_code:
            cursor.execute('SELECT id, uses_left FROM friend_codes WHERE code = ? AND (expires_at IS NULL OR expires_at > CURRENT_TIMESTAMP)', (friend_code,))
            code_row = cursor.fetchone()
            if code_row and (code_row['uses_left'] > 0 or code_row['uses_left'] == -1):
                plan = 'blackbelt'
                if code_row['uses_left'] > 0:
                    cursor.execute('UPDATE friend_codes SET uses_left = uses_left - 1 WHERE code = ?', (friend_code,))
        
        # Create user
        password_hash = generate_password_hash(password)
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, plan, friend_code_used)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, email, password_hash, plan, friend_code if friend_code else None))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Set session
        session['user_id'] = user_id
        session['username'] = username
        session['plan'] = plan
        
        return jsonify({
            'success': True,
            'message': f'Account created successfully! Welcome to BJJ AI Analyzer!',
            'redirect': '/dashboard'
        })
        
    except Exception as e:
        logger.error(f"Signup error: {str(e)}")
        return jsonify({'success': False, 'message': 'Registration failed. Please try again.'})

@app.route('/login', methods=['POST'])
def login():
    """User login"""
    try:
        data = request.get_json() or request.form
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({'success': False, 'message': 'Please enter username and password'})
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Find user
        cursor.execute('SELECT id, username, password_hash, plan FROM users WHERE username = ? OR email = ?', (username, username))
        user = cursor.fetchone()
        conn.close()
        
        if not user or not check_password_hash(user['password_hash'], password):
            return jsonify({'success': False, 'message': 'Invalid username or password'})
        
        # Set session
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['plan'] = user['plan']
        
        return jsonify({
            'success': True,
            'message': 'Login successful!',
            'redirect': '/dashboard'
        })
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'success': False, 'message': 'Login failed. Please try again.'})

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get user stats
    cursor.execute('SELECT COUNT(*) FROM videos WHERE user_id = ?', (session['user_id'],))
    total_videos = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM analysis_results WHERE video_id IN (SELECT id FROM videos WHERE user_id = ?)', (session['user_id'],))
    total_techniques = cursor.fetchone()[0]
    
    # Get recent videos
    cursor.execute('''
        SELECT id, original_filename, upload_timestamp, analysis_complete, duration
        FROM videos WHERE user_id = ?
        ORDER BY upload_timestamp DESC LIMIT 5
    ''', (session['user_id'],))
    recent_videos = cursor.fetchall()
    
    # Get active challenges
    cursor.execute('SELECT id, title, description, points, challenge_type FROM challenges WHERE active = TRUE LIMIT 6')
    challenges = cursor.fetchall()
    
    conn.close()
    
    return render_template('dashboard.html', 
                         total_videos=total_videos,
                         total_techniques=total_techniques,
                         recent_videos=recent_videos,
                         challenges=challenges,
                         user_plan=session.get('plan', 'free'))

@app.route('/upload', methods=['POST'])
@login_required
def upload_video():
    """Handle video upload"""
    try:
        # Check file upload
        if 'video' not in request.files:
            return jsonify({'success': False, 'message': 'No video file uploaded'})
        
        file = request.files['video']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'})
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'message': 'Invalid file type. Please upload MP4, AVI, MOV, MKV, or WEBM files.'})
        
        # Check monthly upload limit for free users
        user_plan = session.get('plan', 'free')
        if user_plan == 'free':
            current_month = datetime.now().strftime('%Y-%m')
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT monthly_uploads, last_upload_month FROM users WHERE id = ?
            ''', (session['user_id'],))
            user_data = cursor.fetchone()
            
            monthly_uploads = user_data['monthly_uploads'] if user_data['last_upload_month'] == current_month else 0
            if monthly_uploads >= 3:  # Free limit
                conn.close()
                return jsonify({'success': False, 'message': 'Monthly upload limit reached. Upgrade to Pro or Black Belt for unlimited uploads.'})
        
        # Save file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Get video info
        cap = cv2.VideoCapture(filepath)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        duration = frame_count / fps if fps > 0 else 0
        file_size = os.path.getsize(filepath)
        cap.release()
        
        # Save to database
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO videos (user_id, filename, original_filename, duration, file_size)
            VALUES (?, ?, ?, ?, ?)
        ''', (session['user_id'], filename, file.filename, duration, file_size))
        
        video_id = cursor.lastrowid
        
        # Update user upload count
        current_month = datetime.now().strftime('%Y-%m')
        cursor.execute('''
            UPDATE users SET 
                total_uploads = total_uploads + 1,
                monthly_uploads = CASE 
                    WHEN last_upload_month = ? THEN monthly_uploads + 1 
                    ELSE 1 
                END,
                last_upload_month = ?
            WHERE id = ?
        ''', (current_month, current_month, session['user_id']))
        
        conn.commit()
        conn.close()
        
        # Start analysis in background
        analysis_result = bjj_ai.analyze_video(filepath, user_plan, session['user_id'])
        
        # Save analysis results
        if analysis_result and analysis_result.get('techniques'):
            conn = get_db()
            cursor = conn.cursor()
            
            # Mark video as analyzed
            cursor.execute('UPDATE videos SET analysis_complete = TRUE, analysis_data = ? WHERE id = ?', 
                         (json.dumps(analysis_result), video_id))
            
            # Save individual technique detections
            for technique in analysis_result['techniques']:
                cursor.execute('''
                    INSERT INTO analysis_results 
                    (video_id, technique_name, category, confidence, start_time, end_time, position, quality_score, clip_path)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (video_id, technique['name'], technique['category'], technique['confidence'],
                     technique['start_time'], technique['end_time'], technique.get('position'),
                     technique.get('quality_score'), technique.get('clip_path')))
            
            conn.commit()
            conn.close()
        
        return jsonify({
            'success': True,
            'message': f'Video uploaded and analyzed successfully! Found {len(analysis_result.get("techniques", []))} techniques.',
            'video_id': video_id,
            'techniques_found': len(analysis_result.get('techniques', [])),
            'analysis_result': analysis_result
        })
        
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return jsonify({'success': False, 'message': f'Upload failed: {str(e)}'})

@app.route('/youtube', methods=['POST'])
@login_required
def analyze_youtube():
    """Analyze YouTube video"""
    try:
        data = request.get_json() or request.form
        youtube_url = data.get('youtube_url', '').strip()
        
        if not youtube_url:
            return jsonify({'success': False, 'message': 'Please enter a YouTube URL'})
        
        # Process YouTube video
        video_info = youtube_processor.download_and_process(youtube_url)
        if not video_info['success']:
            return jsonify({'success': False, 'message': video_info['message']})
        
        # Save to database
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO videos (user_id, youtube_url, original_filename, duration, file_size)
            VALUES (?, ?, ?, ?, ?)
        ''', (session['user_id'], youtube_url, video_info['title'], 
              video_info.get('duration', 0), video_info.get('file_size', 0)))
        
        video_id = cursor.lastrowid
        
        # Analyze video
        user_plan = session.get('plan', 'free')
        analysis_result = bjj_ai.analyze_video(video_info['filepath'], user_plan, session['user_id'])
        
        # Save analysis results
        if analysis_result and analysis_result.get('techniques'):
            cursor.execute('UPDATE videos SET analysis_complete = TRUE, analysis_data = ? WHERE id = ?', 
                         (json.dumps(analysis_result), video_id))
            
            for technique in analysis_result['techniques']:
                cursor.execute('''
                    INSERT INTO analysis_results 
                    (video_id, technique_name, category, confidence, start_time, end_time, position, quality_score)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (video_id, technique['name'], technique['category'], technique['confidence'],
                     technique['start_time'], technique['end_time'], technique.get('position'),
                     technique.get('quality_score')))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': f'YouTube video analyzed successfully! Found {len(analysis_result.get("techniques", []))} techniques.',
            'analysis_result': analysis_result
        })
        
    except Exception as e:
        logger.error(f"YouTube analysis error: {str(e)}")
        return jsonify({'success': False, 'message': f'YouTube analysis failed: {str(e)}'})

@app.route('/results/<int:video_id>')
@login_required
def view_results(video_id):
    """View analysis results"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get video info
    cursor.execute('SELECT * FROM videos WHERE id = ? AND user_id = ?', (video_id, session['user_id']))
    video = cursor.fetchone()
    
    if not video:
        flash('Video not found')
        return redirect(url_for('dashboard'))
    
    # Get analysis results
    cursor.execute('''
        SELECT * FROM analysis_results WHERE video_id = ?
        ORDER BY start_time
    ''', (video_id,))
    techniques = cursor.fetchall()
    
    conn.close()
    
    # Parse analysis data
    analysis_data = {}
    if video['analysis_data']:
        analysis_data = json.loads(video['analysis_data'])
    
    return render_template('results.html', video=video, techniques=techniques, analysis_data=analysis_data)

@app.route('/challenges')
@login_required
def challenges():
    """Challenges page"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get all active challenges
    cursor.execute('SELECT * FROM challenges WHERE active = TRUE ORDER BY challenge_type, difficulty')
    all_challenges = cursor.fetchall()
    
    # Get user's completed challenges
    cursor.execute('''
        SELECT challenge_id, completed_at, points_earned FROM challenge_completions 
        WHERE user_id = ?
    ''', (session['user_id'],))
    completed = {row['challenge_id']: row for row in cursor.fetchall()}
    
    conn.close()
    
    return render_template('challenges.html', challenges=all_challenges, completed=completed)

@app.route('/profile')
@login_required
def profile():
    """User profile page"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get user info
    cursor.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],))
    user = cursor.fetchone()
    
    # Get user stats
    cursor.execute('SELECT COUNT(*) FROM videos WHERE user_id = ?', (session['user_id'],))
    total_videos = cursor.fetchone()[0]
    
    cursor.execute('''
        SELECT COUNT(*) FROM analysis_results 
        WHERE video_id IN (SELECT id FROM videos WHERE user_id = ?)
    ''', (session['user_id'],))
    total_techniques = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM challenge_completions WHERE user_id = ?', (session['user_id'],))
    completed_challenges = cursor.fetchone()[0]
    
    # Get user's friend codes
    cursor.execute('SELECT code, uses_left, created_at FROM friend_codes WHERE created_by = ?', (session['user_id'],))
    friend_codes = cursor.fetchall()
    
    conn.close()
    
    return render_template('profile.html', 
                         user=user, 
                         total_videos=total_videos,
                         total_techniques=total_techniques,
                         completed_challenges=completed_challenges,
                         friend_codes=friend_codes)

@app.route('/leaderboards')
@login_required
def leaderboards():
    """Leaderboards page"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Top users by points
    cursor.execute('''
        SELECT username, points, plan FROM users 
        ORDER BY points DESC LIMIT 20
    ''', )
    top_points = cursor.fetchall()
    
    # Top users by uploads
    cursor.execute('''
        SELECT username, total_uploads, plan FROM users 
        ORDER BY total_uploads DESC LIMIT 20
    ''')
    top_uploads = cursor.fetchall()
    
    # Top users by techniques detected
    cursor.execute('''
        SELECT u.username, COUNT(ar.id) as technique_count, u.plan
        FROM users u
        JOIN videos v ON u.id = v.user_id
        JOIN analysis_results ar ON v.id = ar.video_id
        GROUP BY u.id
        ORDER BY technique_count DESC LIMIT 20
    ''')
    top_techniques = cursor.fetchall()
    
    conn.close()
    
    return render_template('leaderboards.html',
                         top_points=top_points,
                         top_uploads=top_uploads, 
                         top_techniques=top_techniques)

@app.route('/generate_friend_code', methods=['POST'])
@login_required
def generate_friend_code():
    """Generate friend code for Black Belt users"""
    user_plan = session.get('plan', 'free')
    if user_plan != 'blackbelt':
        return jsonify({'success': False, 'message': 'Only Black Belt users can generate friend codes'})
    
    try:
        friend_code = 'BJJ' + secrets.token_urlsafe(8).upper()
        expires_at = datetime.now() + timedelta(days=30)
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO friend_codes (code, created_by, uses_left, expires_at)
            VALUES (?, ?, ?, ?)
        ''', (friend_code, session['user_id'], 5, expires_at))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'friend_code': friend_code})
        
    except Exception as e:
        logger.error(f"Friend code generation error: {str(e)}")
        return jsonify({'success': False, 'message': 'Failed to generate friend code'})

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# Initialize database on startup
@app.before_first_request
def create_tables():
    init_database()

if __name__ == '__main__':
    init_database()
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
