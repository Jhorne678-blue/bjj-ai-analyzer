from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash, send_file
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
    
    # Challenges table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS challenges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            points INTEGER DEFAULT 10,
            type TEXT DEFAULT 'daily',
            active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # User challenge completions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_challenges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            challenge_id INTEGER,
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
            user_id INTEGER,
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
    
    # Technique learning table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS technique_learning (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            technique_name TEXT NOT NULL,
            category TEXT NOT NULL,
            detection_count INTEGER DEFAULT 0,
            accuracy_sum REAL DEFAULT 0.0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ai_improvements TEXT DEFAULT '{}'
        )
    ''')
    
    # Insert default challenges if table is empty
    cursor.execute('SELECT COUNT(*) FROM challenges')
    if cursor.fetchone()[0] == 0:
        default_challenges = [
            ("Daily Drill: Armbar from Guard", "Practice 10 clean armbar setups from closed guard", "submissions", "beginner", 10, "daily"),
            ("Weekly Flow: Guard Retention", "Demonstrate 5 different guard retention techniques", "guard_retention", "intermediate", 25, "weekly"),
            ("Monthly Master: Competition Prep", "Upload a 10-minute sparring session with analysis", "sparring", "advanced", 100, "monthly"),
            ("Solo Flow: Shrimping", "Perform 20 perfect shrimps in sequence", "movement", "beginner", 15, "daily"),
            ("Partner Drill: Takedown Defense", "Practice takedown defense for 5 minutes with partner", "takedowns", "intermediate", 20, "daily"),
            ("Black Belt Challenge: Berimbolo", "Execute 3 berimbolo sweeps in live rolling", "sweeps", "expert", 50, "weekly")
        ]
        
        for challenge in default_challenges:
            cursor.execute('''
                INSERT INTO challenges (title, description, category, difficulty, points, type)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', challenge)
    
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
    cursor.execute('SELECT plan, subscription_expires FROM users WHERE id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        plan, expires = result
        if expires and datetime.fromisoformat(expires) < datetime.now():
            # Subscription expired, downgrade to free
            conn = sqlite3.connect('bjj_analyzer.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET plan = "free", subscription_expires = NULL WHERE id = ?', (user_id,))
            conn.commit()
            conn.close()
            return 'free'
        return plan
    return 'free'

def can_upload(user_id):
    plan = get_user_plan(user_id)
    if plan == 'blackbelt':
        return True, "Unlimited uploads"
    
    conn = sqlite3.connect('bjj_analyzer.db')
    cursor = conn.cursor()
    
    current_month = datetime.now().strftime('%Y-%m')
    cursor.execute('SELECT monthly_uploads, last_upload_month FROM users WHERE id = ?', (user_id,))
    result = cursor.fetchone()
    
    if result:
        monthly_uploads, last_month = result
        
        # Reset monthly count if new month
        if last_month != current_month:
            cursor.execute('UPDATE users SET monthly_uploads = 0, last_upload_month = ? WHERE id = ?', 
                         (current_month, user_id))
            conn.commit()
            monthly_uploads = 0
        
        limits = {'free': 1, 'pro': 4, 'blackbelt': float('inf')}
        limit = limits.get(plan, 1)
        
        conn.close()
        return monthly_uploads < limit, f"{monthly_uploads}/{limit} uploads this month"
    
    conn.close()
    return False, "User not found"

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

@app.route('/auth/facebook')
def facebook_login():
    redirect_uri = url_for('facebook_callback', _external=True)
    return facebook.authorize_redirect(redirect_uri)

@app.route('/auth/facebook/callback')
def facebook_callback():
    token = facebook.authorize_access_token()
    user_info = facebook.parse_id_token(token)
    
    conn = sqlite3.connect('bjj_analyzer.db')
    cursor = conn.cursor()
    
    # Check if user exists with this Facebook ID
    cursor.execute('SELECT id, username FROM users WHERE facebook_id = ?', (user_info['sub'],))
    user = cursor.fetchone()
    
    if user:
        session['user_id'] = user[0]
        session['username'] = user[1]
    else:
        # Create new user
        username = user_info.get('name', f"user_{user_info['sub'][:8]}")
        email = user_info.get('email', f"{user_info['sub']}@facebook.com")
        
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, facebook_id, last_upload_month)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, email, 'facebook_user', user_info['sub'], datetime.now().strftime('%Y-%m')))
        
        user_id = cursor.lastrowid
        session['user_id'] = user_id
        session['username'] = username
    
    conn.commit()
    conn.close()
    
    flash('Logged in with Facebook successfully!')
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    plan = get_user_plan(user_id)
    can_upload_status, upload_message = can_upload(user_id)
    
    # Get user stats
    conn = sqlite3.connect('bjj_analyzer.db')
    cursor = conn.cursor()
    
    # Total videos and techniques
    cursor.execute('SELECT COUNT(*) FROM videos WHERE user_id = ?', (user_id,))
    total_videos = cursor.fetchone()[0]
    
    cursor.execute('''
        SELECT COUNT(*) FROM analysis_results ar
        JOIN videos v ON ar.video_id = v.id
        WHERE v.user_id = ?
    ''', (user_id,))
    total_techniques = cursor.fetchone()[0]
    
    # Recent challenges
    cursor.execute('''
        SELECT c.title, c.description, c.points, c.difficulty, c.type
        FROM challenges c
        WHERE c.active = 1
        ORDER BY c.created_at DESC
        LIMIT 6
    ''', ())
    challenges = cursor.fetchall()
    
    # Recent videos
    cursor.execute('''
        SELECT filename, original_filename, upload_timestamp, analysis_complete
        FROM videos
        WHERE user_id = ?
        ORDER BY upload_timestamp DESC
        LIMIT 5
    ''', (user_id,))
    recent_videos = cursor.fetchall()
    
    conn.close()
    
    return render_template('dashboard.html', 
                         plan=plan, 
                         can_upload=can_upload_status,
                         upload_message=upload_message,
                         total_videos=total_videos,
                         total_techniques=total_techniques,
                         challenges=challenges,
                         recent_videos=recent_videos)

@app.route('/upload', methods=['POST'])
@login_required
def upload_video():
    user_id = session['user_id']
    can_upload_status, message = can_upload(user_id)
    
    if not can_upload_status:
        return jsonify({'error': message}), 403
    
    if 'video' not in request.files and 'youtube_url' not in request.form:
        return jsonify({'error': 'No video file or YouTube URL provided'}), 400
    
    video_id = None
    
    # Handle file upload
    if 'video' in request.files:
        file = request.files['video']
        if file.filename != '' and allowed_file(file.filename):
            filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Save to database
            conn = sqlite3.connect('bjj_analyzer.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO videos (user_id, filename, original_filename, file_size)
                VALUES (?, ?, ?, ?)
            ''', (user_id, filename, file.filename, os.path.getsize(filepath)))
            video_id = cursor.lastrowid
            conn.commit()
            conn.close()
    
    # Handle YouTube URL
    elif 'youtube_url' in request.form:
        youtube_url = request.form['youtube_url']
        
        try:
            # Download YouTube video
            ydl_opts = {
                'format': 'best[height<=720]',
                'outtmpl': os.path.join(app.config['UPLOAD_FOLDER'], '%(id)s.%(ext)s'),
                'quiet': True
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(youtube_url, download=True)
                filename = f"{info['id']}.{info['ext']}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                
                # Save to database
                conn = sqlite3.connect('bjj_analyzer.db')
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO videos (user_id, filename, youtube_url, file_size, duration)
                    VALUES (?, ?, ?, ?, ?)
                ''', (user_id, filename, youtube_url, os.path.getsize(filepath), info.get('duration', 0)))
                video_id = cursor.lastrowid
                conn.commit()
                conn.close()
                
        except Exception as e:
            return jsonify({'error': f'Failed to download YouTube video: {str(e)}'}), 400
    
    if video_id:
        # Update monthly upload count
        conn = sqlite3.connect('bjj_analyzer.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET monthly_uploads = monthly_uploads + 1, total_uploads = total_uploads + 1 WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
        
        # Start analysis in background
        threading.Thread(target=analyze_video_background, args=(video_id, user_id)).start()
        
        return jsonify({'success': True, 'video_id': video_id, 'message': 'Upload successful! Analysis starting...'})
    
    return jsonify({'error': 'Upload failed'}), 400

def analyze_video_background(video_id, user_id):
    """Background task to analyze video"""
    try:
        conn = sqlite3.connect('bjj_analyzer.db')
        cursor = conn.cursor()
        
        # Get video info
        cursor.execute('SELECT filename FROM videos WHERE id = ?', (video_id,))
        result = cursor.fetchone()
        if not result:
            return
        
        filename = result[0]
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Run analysis
        plan = get_user_plan(user_id)
        results = analyzer.analyze_video(filepath, plan)
        
        # Save results to database
        for technique in results['techniques']:
            cursor.execute('''
                INSERT INTO analysis_results 
                (video_id, technique_name, category, confidence, start_time, end_time, position, quality_score, clip_path)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                video_id,
                technique['name'],
                technique['category'],
                technique['confidence'],
                technique['start_time'],
                technique['end_time'],
                technique.get('position', ''),
                technique.get('quality_score', 0),
                technique.get('clip_path', '')
            ))
        
        # Update video as analyzed
        cursor.execute('UPDATE videos SET analysis_complete = 1, duration = ? WHERE id = ?', 
                      (results.get('duration', 0), video_id))
        
        # Update AI learning
        for technique in results['techniques']:
            cursor.execute('''
                INSERT OR REPLACE INTO technique_learning 
                (technique_name, category, detection_count, accuracy_sum, last_updated)
                VALUES (?, ?, 
                    COALESCE((SELECT detection_count FROM technique_learning WHERE technique_name = ?), 0) + 1,
                    COALESCE((SELECT accuracy_sum FROM technique_learning WHERE technique_name = ?), 0) + ?,
                    CURRENT_TIMESTAMP)
            ''', (technique['name'], technique['category'], technique['name'], technique['name'], technique['confidence']))
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"Analysis error: {e}")
        # Mark analysis as failed
        conn = sqlite3.connect('bjj_analyzer.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE videos SET analysis_complete = 0 WHERE id = ?', (video_id,))
        conn.commit()
        conn.close()

@app.route('/results/<int:video_id>')
@login_required
def results(video_id):
    user_id = session['user_id']
    
    conn = sqlite3.connect('bjj_analyzer.db')
    cursor = conn.cursor()
    
    # Verify user owns this video
    cursor.execute('SELECT filename, original_filename, analysis_complete, duration FROM videos WHERE id = ? AND user_id = ?', 
                  (video_id, user_id))
    video = cursor.fetchone()
    
    if not video:
        flash('Video not found')
        return redirect(url_for('dashboard'))
    
    if not video[2]:  # analysis_complete
        return render_template('analysis_pending.html', video_id=video_id)
    
    # Get analysis results
    cursor.execute('''
        SELECT technique_name, category, confidence, start_time, end_time, position, quality_score, clip_path
        FROM analysis_results
        WHERE video_id = ?
        ORDER BY start_time
    ''', (video_id,))
    
    techniques = cursor.fetchall()
    conn.close()
    
    # Format results
    formatted_techniques = []
    for tech in techniques:
        formatted_techniques.append({
            'name': tech[0],
            'category': tech[1],
            'confidence': tech[2],
            'start_time': tech[3],
            'end_time': tech[4],
            'position': tech[5],
            'quality_score': tech[6],
            'clip_path': tech[7]
        })
    
    plan = get_user_plan(user_id)
    
    return render_template('results.html', 
                         video=video, 
                         techniques=formatted_techniques, 
                         plan=plan,
                         video_id=video_id)

@app.route('/use_code', methods=['POST'])
@login_required
def use_black_belt_code():
    code = request.form.get('code', '').strip().upper()
    user_id = session['user_id']
    
    if code not in BLACK_BELT_CODES:
        return jsonify({'error': 'Invalid code'}), 400
    
    code_info = BLACK_BELT_CODES[code]
    
    # Check if code is expired
    if datetime.now() > datetime.fromisoformat(code_info['expires']):
        return jsonify({'error': 'Code has expired'}), 400
    
    # Check if code has uses left
    if code_info['uses_left'] == 0:
        return jsonify({'error': 'Code has no uses remaining'}), 400
    
    # Apply black belt access
    conn = sqlite3.connect('bjj_analyzer.db')
    cursor = conn.cursor()
    
    # Set expiration to 1 year from now
    expires = (datetime.now() + timedelta(days=365)).isoformat()
    
    cursor.execute('''
        UPDATE users 
        SET plan = 'blackbelt', subscription_expires = ?, black_belt_code = ?
        WHERE id = ?
    ''', (expires, code, user_id))
    
    conn.commit()
    conn.close()
    
    # Decrease code uses (if not unlimited)
    if code_info['uses_left'] > 0:
        BLACK_BELT_CODES[code]['uses_left'] -= 1
    
    return jsonify({'success': True, 'message': 'Black Belt access activated!'})

@app.route('/subscribe/<plan>')
@login_required
def subscribe(plan):
    if plan not in ['pro', 'blackbelt']:
        flash('Invalid plan')
        return redirect(url_for('dashboard'))
    
    prices = {'pro': 29.99, 'blackbelt': 59.99}
    price = prices[plan]
    
    # Create PayPal payment
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": url_for('payment_success', _external=True),
            "cancel_url": url_for('payment_cancel', _external=True)
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": f"BJJ Analyzer {plan.title()} Plan",
                    "sku": plan,
                    "price": str(price),
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": str(price),
                "currency": "USD"
            },
            "description": f"Monthly subscription to BJJ Analyzer {plan.title()} plan"
        }]
    })
    
    if payment.create():
        # Store payment info in session
        session['pending_payment'] = {
            'payment_id': payment.id,
            'plan': plan,
            'amount': price
        }
        
        # Redirect to PayPal
        for link in payment.links:
            if link.rel == "approval_url":
                return redirect(link.href)
    
    flash('Payment creation failed')
    return redirect(url_for('dashboard'))

@app.route('/payment/success')
@login_required
def payment_success():
    payment_id = request.args.get('paymentId')
    payer_id = request.args.get('PayerID')
    
    if 'pending_payment' not in session or session['pending_payment']['payment_id'] != payment_id:
        flash('Payment verification failed')
        return redirect(url_for('dashboard'))
    
    payment = paypalrestsdk.Payment.find(payment_id)
    
    if payment.execute({"payer_id": payer_id}):
        # Payment successful, upgrade user
        plan = session['pending_payment']['plan']
        amount = session['pending_payment']['amount']
        user_id = session['user_id']
        
        # Set subscription expiration to 1 month from now
        expires = (datetime.now() + timedelta(days=30)).isoformat()
        
        conn = sqlite3.connect('bjj_analyzer.db')
        cursor = conn.cursor()
        
        # Update user plan
        cursor.execute('''
            UPDATE users 
            SET plan = ?, subscription_expires = ?, payment_method = 'paypal'
            WHERE id = ?
        ''', (plan, expires, user_id))
        
        # Record payment
        cursor.execute('''
            INSERT INTO payments (user_id, amount, plan, payment_method, transaction_id, status)
            VALUES (?, ?, ?, 'paypal', ?, 'completed')
        ''', (user_id, amount, plan, payment_id))
        
        conn.commit()
        conn.close()
        
        # Clear session
        session.pop('pending_payment', None)
        
        flash(f'Successfully upgraded to {plan.title()} plan!')
    else:
        flash('Payment execution failed')
    
    return redirect(url_for('dashboard'))

@app.route('/payment/cancel')
@login_required
def payment_cancel():
    session.pop('pending_payment', None)
    flash('Payment cancelled')
    return redirect(url_for('dashboard'))

@app.route('/challenges')
@login_required
def challenges():
    conn = sqlite3.connect('bjj_analyzer.db')
    cursor = conn.cursor()
    
    # Get all active challenges
    cursor.execute('''
        SELECT id, title, description, category, difficulty, points, type
        FROM challenges
        WHERE active = 1
        ORDER BY type, difficulty, created_at DESC
    ''', ())
    all_challenges = cursor.fetchall()
    
    # Get user's completed challenges
    user_id = session['user_id']
    cursor.execute('''
        SELECT challenge_id, completed_at, points_earned
        FROM user_challenges
        WHERE user_id = ?
    ''', (user_id,))
    completed = {row[0]: {'completed_at': row[1], 'points': row[2]} for row in cursor.fetchall()}
    
    conn.close()
    
    # Group challenges by type
    challenges_by_type = {'daily': [], 'weekly': [], 'monthly': []}
    for challenge in all_challenges:
        challenge_data = {
            'id': challenge[0],
            'title': challenge[1],
            'description': challenge[2],
            'category': challenge[3],
            'difficulty': challenge[4],
            'points': challenge[5],
            'type': challenge[6],
            'completed': challenge[0] in completed,
            'completed_info': completed.get(challenge[0], {})
        }
        challenges_by_type[challenge[6]].append(challenge_data)
    
    return render_template('challenges.html', challenges=challenges_by_type)

@app.route('/api/analysis_status/<int:video_id>')
@login_required
def analysis_status(video_id):
    user_id = session['user_id']
    
    conn = sqlite3.connect('bjj_analyzer.db')
    cursor = conn.cursor()
    cursor.execute('SELECT analysis_complete FROM videos WHERE id = ? AND user_id = ?', (video_id, user_id))
    result = cursor.fetchone()
    conn.close()
    
@app.route('/api/analysis_status/<int:video_id>')
@login_required
def analysis_status(video_id):
    user_id = session['user_id']
    
    conn = sqlite3.connect('bjj_analyzer.db')
    cursor = conn.cursor()
    cursor.execute('SELECT analysis_complete FROM videos WHERE id = ? AND user_id = ?', (video_id, user_id))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return jsonify({'complete': bool(result[0])})
    return jsonify({'error': 'Video not found'}), 404

@app.route('/download_clip/<int:video_id>/<technique_name>')
@login_required
def download_clip(video_id, technique_name):
    user_id = session['user_id']
    plan = get_user_plan(user_id)
    
    if plan != 'blackbelt':
        return jsonify({'error': 'Clip downloads require Black Belt plan'}), 403
    
    conn = sqlite3.connect('bjj_analyzer.db')
    cursor = conn.cursor()
    
    # Verify user owns this video and get clip path
    cursor.execute('''
        SELECT ar.clip_path FROM analysis_results ar
        JOIN videos v ON ar.video_id = v.id
        WHERE v.id = ? AND v.user_id = ? AND ar.technique_name = ?
    ''', (video_id, user_id, technique_name))
    
    result = cursor.fetchone()
    conn.close()
    
    if result and result[0] and os.path.exists(result[0]):
        return send_file(result[0], as_attachment=True)
    
    return jsonify({'error': 'Clip not found'}), 404

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('DEBUG', 'False').lower() == 'true')
