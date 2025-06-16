from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import os
import json
import secrets
import logging
from datetime import datetime, timedelta
from analyzer import BJJAnalyzer

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

# Initialize BJJ Analyzer
bjj_analyzer = BJJAnalyzer()

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
    
    # Videos table - Enhanced with analysis data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT,
            original_filename TEXT,
            upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            analysis_complete BOOLEAN DEFAULT FALSE,
            analysis_data TEXT,
            total_techniques INTEGER DEFAULT 0,
            average_confidence REAL DEFAULT 0.0,
            duration REAL DEFAULT 0.0,
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
                <p class="text-gray-600 mb-6">Professional Brazilian Jiu-Jitsu Video Analysis with 100+ Techniques</p>
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
    """Enhanced dashboard with upload functionality"""
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
                        <div class="text-2xl font-bold text-purple-600" id="videos-count">0</div>
                        <div class="text-sm text-gray-600">Videos Uploaded</div>
                    </div>
                    <div class="bg-white rounded-xl shadow-md p-6">
                        <div class="text-2xl font-bold text-green-600" id="techniques-count">0</div>
                        <div class="text-sm text-gray-600">Techniques Detected</div>
                    </div>
                    <div class="bg-white rounded-xl shadow-md p-6">
                        <div class="text-2xl font-bold text-yellow-600">Free</div>
                        <div class="text-sm text-gray-600">Current Plan</div>
                    </div>
                </div>
                
                <div class="bg-white rounded-xl shadow-md p-8 mb-8">
                    <h2 class="text-xl font-semibold mb-4">Upload BJJ Training Video</h2>
                    <div id="upload-area" class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center cursor-pointer hover:border-purple-400 transition-colors">
                        <div class="text-4xl mb-4">🎥</div>
                        <p class="text-lg text-gray-600 mb-2">Click to upload or drag and drop your BJJ training video</p>
                        <p class="text-sm text-gray-500">MP4, AVI, MOV supported (max 500MB)</p>
                        <input type="file" id="video-input" accept=".mp4,.avi,.mov,.mkv,.webm" class="hidden">
                        <div id="upload-progress" class="hidden mt-4">
                            <div class="bg-gray-200 rounded-full h-2">
                                <div id="progress-bar" class="bg-purple-600 h-2 rounded-full" style="width: 0%"></div>
                            </div>
                            <p class="text-sm text-gray-600 mt-2">Uploading and analyzing...</p>
                        </div>
                    </div>
                </div>
                
                <div id="recent-videos" class="bg-white rounded-xl shadow-md p-8">
                    <h2 class="text-xl font-semibold mb-4">Recent Analyses</h2>
                    <div id="video-list" class="space-y-4">
                        <p class="text-gray-500 text-center py-4">No videos uploaded yet. Upload your first BJJ training video to get started!</p>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
        const uploadArea = document.getElementById('upload-area');
        const videoInput = document.getElementById('video-input');
        const uploadProgress = document.getElementById('upload-progress');
        const progressBar = document.getElementById('progress-bar');
        
        // Click to upload
        uploadArea.addEventListener('click', () => videoInput.click());
        
        // Drag and drop functionality
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('border-purple-400', 'bg-purple-50');
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('border-purple-400', 'bg-purple-50');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('border-purple-400', 'bg-purple-50');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                handleFileUpload(files[0]);
            }
        });
        
        // File input change
        videoInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                handleFileUpload(e.target.files[0]);
            }
        });
        
        async function handleFileUpload(file) {
            // Validate file
            const allowedTypes = ['video/mp4', 'video/avi', 'video/mov', 'video/quicktime', 'video/x-msvideo', 'video/webm'];
            if (!allowedTypes.includes(file.type)) {
                alert('Please upload a valid video file (MP4, AVI, MOV, WEBM)');
                return;
            }
            
            if (file.size > 500 * 1024 * 1024) {
                alert('File size must be less than 500MB');
                return;
            }
            
            // Show progress
            uploadProgress.classList.remove('hidden');
            uploadArea.style.display = 'none';
            
            const formData = new FormData();
            formData.append('video', file);
            
            try {
                // Simulate progress
                let progress = 0;
                const progressInterval = setInterval(() => {
                    progress += Math.random() * 15;
                    if (progress > 90) progress = 90;
                    progressBar.style.width = progress + '%';
                }, 500);
                
                const response = await fetch('/upload_video', {
                    method: 'POST',
                    body: formData
                });
                
                clearInterval(progressInterval);
                progressBar.style.width = '100%';
                
                const result = await response.json();
                
                if (result.success) {
                    setTimeout(() => {
                        window.location.href = '/analysis/' + result.video_id;
                    }, 1000);
                } else {
                    alert('Upload failed: ' + result.message);
                    resetUpload();
                }
            } catch (error) {
                alert('Upload failed. Please try again.');
                resetUpload();
            }
        }
        
        function resetUpload() {
            uploadProgress.classList.add('hidden');
            uploadArea.style.display = 'block';
            progressBar.style.width = '0%';
            videoInput.value = '';
        }
        </script>
    </body>
    </html>
    '''

@app.route('/upload_video', methods=['POST'])
def upload_video():
    """Handle video upload and analysis"""
    try:
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': 'Please log in first'})
        
        if 'video' not in request.files:
            return jsonify({'success': False, 'message': 'No video file provided'})
        
        file = request.files['video']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'})
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'message': 'Invalid file type'})
        
        # Secure filename and save
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        unique_filename = timestamp + filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        file.save(filepath)
        logger.info(f"Video saved: {filepath}")
        
        # Get user plan for analysis
        user_id = session['user_id']
        plan = session.get('plan', 'free')
        
        # Analyze video with BJJ AI
        analysis_result = bjj_analyzer.analyze_video(filepath, plan, user_id)
        
        # Save to database
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO videos (user_id, filename, original_filename, analysis_complete, 
                              analysis_data, total_techniques, average_confidence, duration)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id, unique_filename, filename, True,
            json.dumps(analysis_result), analysis_result.get('total_techniques', 0),
            analysis_result.get('average_confidence', 0.0), analysis_result.get('duration', 0.0)
        ))
        
        video_id = cursor.lastrowid
        
        # Update user stats
        cursor.execute('UPDATE users SET total_uploads = total_uploads + 1 WHERE id = ?', (user_id,))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True, 
            'message': 'Video analyzed successfully!',
            'video_id': video_id,
            'analysis': analysis_result
        })
        
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return jsonify({'success': False, 'message': 'Upload failed. Please try again.'})

@app.route('/analysis/<int:video_id>')
def analysis_results(video_id):
    """Display comprehensive analysis results with tabs"""
    try:
        if 'user_id' not in session:
            return redirect(url_for('auth'))
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Get video and analysis data
        cursor.execute('''
            SELECT * FROM videos WHERE id = ? AND user_id = ?
        ''', (video_id, session['user_id']))
        
        video = cursor.fetchone()
        if not video:
            return redirect(url_for('dashboard'))
        
        analysis_data = json.loads(video['analysis_data'])
        conn.close()
        
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Analysis Results - BJJ AI Analyzer</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <script src="https://cdn.tailwindcss.com"></script>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body class="bg-gray-50">
            <div class="min-h-screen">
                <nav class="bg-white shadow-lg">
                    <div class="max-w-7xl mx-auto px-4">
                        <div class="flex justify-between items-center h-16">
                            <div class="flex items-center">
                                <span class="text-xl font-bold text-gray-800">🥋 BJJ AI Analyzer</span>
                            </div>
                            <div class="flex items-center space-x-4">
                                <a href="/dashboard" class="text-purple-600 hover:text-purple-800">← Back to Dashboard</a>
                            </div>
                        </div>
                    </div>
                </nav>
                
                <div class="max-w-7xl mx-auto px-4 py-8">
                    <div class="mb-8">
                        <h1 class="text-3xl font-bold text-gray-900 mb-2">Analysis Results</h1>
                        <p class="text-gray-600">Video: {video['original_filename']}</p>
                        <p class="text-sm text-gray-500">Analyzed on {video['upload_timestamp']}</p>
                    </div>
                    
                    <!-- Summary Cards -->
                    <div class="grid md:grid-cols-4 gap-6 mb-8">
                        <div class="bg-white rounded-xl shadow-md p-6 text-center">
                            <div class="text-3xl font-bold text-purple-600">{analysis_data.get('total_techniques', 0)}</div>
                            <div class="text-sm text-gray-600">Total Techniques</div>
                        </div>
                        <div class="bg-white rounded-xl shadow-md p-6 text-center">
                            <div class="text-3xl font-bold text-green-600">{analysis_data.get('average_confidence', 0):.1%}</div>
                            <div class="text-sm text-gray-600">Avg Confidence</div>
                        </div>
                        <div class="bg-white rounded-xl shadow-md p-6 text-center">
                            <div class="text-3xl font-bold text-blue-600">{analysis_data.get('duration', 0):.1f}s</div>
                            <div class="text-sm text-gray-600">Video Duration</div>
                        </div>
                        <div class="bg-white rounded-xl shadow-md p-6 text-center">
                            <div class="text-3xl font-bold text-yellow-600">{analysis_data.get('techniques_per_minute', 0):.1f}</div>
                            <div class="text-sm text-gray-600">Techniques/Min</div>
                        </div>
                    </div>
                    
                    <!-- Tabs Navigation -->
                    <div class="bg-white rounded-t-xl shadow-md">
                        <div class="border-b border-gray-200">
                            <nav class="flex space-x-8 px-6" aria-label="Tabs">
                                <button onclick="showTab('overview')" class="tab-button active border-b-2 border-purple-500 py-4 px-1 text-sm font-medium text-purple-600">
                                    Overview
                                </button>
                                <button onclick="showTab('submissions')" class="tab-button border-b-2 border-transparent py-4 px-1 text-sm font-medium text-gray-500 hover:text-gray-700">
                                    Submissions
                                </button>
                                <button onclick="showTab('sweeps')" class="tab-button border-b-2 border-transparent py-4 px-1 text-sm font-medium text-gray-500 hover:text-gray-700">
                                    Sweeps
                                </button>
                                <button onclick="showTab('takedowns')" class="tab-button border-b-2 border-transparent py-4 px-1 text-sm font-medium text-gray-500 hover:text-gray-700">
                                    Takedowns
                                </button>
                                <button onclick="showTab('overall')" class="tab-button border-b-2 border-transparent py-4 px-1 text-sm font-medium text-gray-500 hover:text-gray-700">
                                    Overall Stats
                                </button>
                            </nav>
                        </div>
                    </div>
                    
                    <!-- Tab Content -->
                    <div class="bg-white rounded-b-xl shadow-md p-6">
                        <!-- Overview Tab -->
                        <div id="overview-tab" class="tab-content">
                            <h2 class="text-2xl font-bold mb-6">Training Session Overview</h2>
                            
                            <div class="grid md:grid-cols-2 gap-8">
                                <div>
                                    <h3 class="text-lg font-semibold mb-4">Category Breakdown</h3>
                                    <div class="space-y-3">
                                        {app._generate_category_breakdown_html(analysis_data.get('category_breakdown', {}))}
                                    </div>
                                </div>
                                
                                <div>
                                    <h3 class="text-lg font-semibold mb-4">Key Insights</h3>
                                    <div class="space-y-2">
                                        {app._generate_insights_html(analysis_data.get('insights', []))}
                                    </div>
                                </div>
                            </div>
                            
                            <div class="mt-8">
                                <h3 class="text-lg font-semibold mb-4">Quality Metrics</h3>
                                <div class="grid md:grid-cols-4 gap-4">
                                    {app._generate_quality_metrics_html(analysis_data.get('quality_metrics', {}))}
                                </div>
                            </div>
                        </div>
                        
                        <!-- Submissions Tab -->
                        <div id="submissions-tab" class="tab-content hidden">
                            <h2 class="text-2xl font-bold mb-6">Submissions Analysis</h2>
                            {app._generate_technique_category_html(analysis_data.get('techniques', []), 'submissions', analysis_data.get('success_analytics', {}), analysis_data.get('failure_analytics', {}))}
                        </div>
                        
                        <!-- Sweeps Tab -->
                        <div id="sweeps-tab" class="tab-content hidden">
                            <h2 class="text-2xl font-bold mb-6">Sweeps Analysis</h2>
                            {app._generate_technique_category_html(analysis_data.get('techniques', []), 'sweeps', analysis_data.get('success_analytics', {}), analysis_data.get('failure_analytics', {}))}
                        </div>
                        
                        <!-- Takedowns Tab -->
                        <div id="takedowns-tab" class="tab-content hidden">
                            <h2 class="text-2xl font-bold mb-6">Takedowns Analysis</h2>
                            {app._generate_technique_category_html(analysis_data.get('techniques', []), 'takedowns', analysis_data.get('success_analytics', {}), analysis_data.get('failure_analytics', {}))}
                        </div>
                        
                        <!-- Overall Tab -->
                        <div id="overall-tab" class="tab-content hidden">
                            <h2 class="text-2xl font-bold mb-6">Complete Technique List</h2>
                            {app._generate_all_techniques_html(analysis_data.get('techniques', []))}
                        </div>
                    </div>
                </div>
            </div>
            
            <script>
            function showTab(tabName) {{
                // Hide all tab contents
                document.querySelectorAll('.tab-content').forEach(tab => {{
                    tab.classList.add('hidden');
                }});
                
                // Remove active class from all buttons
                document.querySelectorAll('.tab-button').forEach(btn => {{
                    btn.classList.remove('active', 'border-purple-500', 'text-purple-600');
                    btn.classList.add('border-transparent', 'text-gray-500');
                }});
                
                // Show selected tab
                document.getElementById(tabName + '-tab').classList.remove('hidden');
                
                // Add active class to clicked button
                event.target.classList.add('active', 'border-purple-500', 'text-purple-600');
                event.target.classList.remove('border-transparent', 'text-gray-500');
            }}
            </script>
        </body>
        </html>
        '''
        
    except Exception as e:
        logger.error(f"Analysis display error: {str(e)}")
        return redirect(url_for('dashboard'))

def _generate_category_breakdown_html(category_breakdown):
    """Generate HTML for category breakdown"""
    html = ""
    for category, data in category_breakdown.items():
        category_name = category.replace('_', ' ').title()
        confidence_pct = data.get('avg_confidence', 0) * 100
        html += f'''
        <div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
            <div>
                <div class="font-medium">{category_name}</div>
                <div class="text-sm text-gray-500">{data.get('count', 0)} techniques</div>
            </div>
            <div class="text-right">
                <div class="font-bold text-purple-600">{confidence_pct:.1f}%</div>
                <div class="text-xs text-gray-500">avg confidence</div>
            </div>
        </div>
        '''
    return html

def _generate_insights_html(insights):
    """Generate HTML for insights"""
    html = ""
    for insight in insights:
        html += f'''
        <div class="flex items-start space-x-2">
            <div class="text-green-500 mt-1">✓</div>
            <div class="text-gray-700">{insight}</div>
        </div>
        '''
    return html

def _generate_quality_metrics_html(quality_metrics):
    """Generate HTML for quality metrics"""
    html = ""
    for metric, value in quality_metrics.items():
        metric_name = metric.replace('_', ' ').title()
        html += f'''
        <div class="text-center">
            <div class="text-2xl font-bold text-blue-600">{value}%</div>
            <div class="text-sm text-gray-600">{metric_name}</div>
        </div>
        '''
    return html

def _generate_technique_category_html(techniques, category, success_analytics, failure_analytics):
    """Generate HTML for specific technique category with success/failure analytics"""
    category_techniques = [t for t in techniques if t.get('category') == category]
    
    if not category_techniques:
        return f'<p class="text-gray-500 text-center py-8">No {category} detected in this video.</p>'
    
    # Get success/failure data for this category
    success_data = success_analytics.get(category, [])
    failure_data = failure_analytics.get(category, [])
    
    html = f'''
    <div class="grid md:grid-cols-2 gap-8 mb-8">
        <!-- Your Success Rates -->
        <div class="bg-green-50 rounded-lg p-6">
            <h3 class="text-lg font-semibold text-green-800 mb-4">📈 Your Success Rates (Best to Worst)</h3>
            {_generate_success_chart_html(success_data)}
        </div>
        
        <!-- What You Get Caught With -->
        <div class="bg-red-50 rounded-lg p-6">
            <h3 class="text-lg font-semibold text-red-800 mb-4">🎯 Most Caught With (Defend Better)</h3>
            {_generate_failure_chart_html(failure_data)}
        </div>
    </div>
    
    <div class="mb-6">
        <div class="text-lg text-gray-600 mb-4">All {len(category_techniques)} {category} techniques detected</div>
    </div>
    <div class="space-y-4">
    '''
    
    for tech in category_techniques:
        confidence_pct = tech.get('confidence', 0) * 100
        start_time = tech.get('start_time', 0)
        end_time = tech.get('end_time', 0)
        is_yours = tech.get('is_your_technique', True)
        outcome = tech.get('outcome', 'Unknown')
        
        # Color coding based on who did it and outcome
        if is_yours:
            outcome_class = 'bg-green-100 text-green-800' if outcome == 'Success' else 'bg-yellow-100 text-yellow-800'
            outcome_prefix = 'Your'
        else:
            outcome_class = 'bg-red-100 text-red-800' if outcome == 'Success' else 'bg-blue-100 text-blue-800'
            outcome_prefix = 'Opponent'
        
        html += f'''
        <div class="border border-gray-200 rounded-lg p-4">
            <div class="flex justify-between items-start mb-2">
                <h3 class="text-lg font-semibold">{tech.get('name', 'Unknown Technique')}</h3>
                <div class="flex space-x-2">
                    <span class="bg-purple-100 text-purple-800 text-sm px-2 py-1 rounded-full">{confidence_pct:.1f}%</span>
                    <span class="{outcome_class} text-sm px-2 py-1 rounded-full">{outcome_prefix} {outcome}</span>
                </div>
            </div>
            <div class="grid md:grid-cols-3 gap-4 text-sm">
                <div>
                    <span class="text-gray-500">Time:</span> {start_time:.1f}s - {end_time:.1f}s
                </div>
                <div>
                    <span class="text-gray-500">Position:</span> {tech.get('position', 'Unknown')}
                </div>
                <div>
                    <span class="text-gray-500">Quality Score:</span> {tech.get('quality_score', 0):.1f}/100
                </div>
            </div>
            <div class="mt-3">
                <div class="text-xs text-gray-500 mb-1">Execution Rating:</div>
                <span class="bg-{_get_rating_color(tech.get('execution_rating', ''))} text-white text-xs px-2 py-1 rounded">
                    {tech.get('execution_rating', 'Unknown')}
                </span>
            </div>
            <div class="mt-3 text-sm text-gray-600">
                <strong>{'Success Tip' if is_yours and outcome == 'Success' else 'Improvement Tip'}:</strong> 
                {tech.get('improvement_tips', 'Keep practicing this technique.')}
            </div>
        </div>
        '''
    
    html += '</div>'
    return html

def _generate_success_chart_html(success_data):
    """Generate HTML for success rate chart"""
    if not success_data:
        return '<p class="text-gray-500 text-center py-4">No data available for this session</p>'
    
    html = '<div class="space-y-3">'
    for i, data in enumerate(success_data[:5]):  # Top 5
        percentage = data['success_rate']
        attempts = data['attempts']
        successes = data['successes']
        
        # Color based on success rate
        if percentage >= 80:
            bar_color = 'bg-green-500'
            text_color = 'text-green-700'
        elif percentage >= 60:
            bar_color = 'bg-yellow-500'
            text_color = 'text-yellow-700'
        else:
            bar_color = 'bg-red-500'
            text_color = 'text-red-700'
        
        html += f'''
        <div class="relative">
            <div class="flex justify-between items-center mb-1">
                <span class="text-sm font-medium truncate">{data['technique']}</span>
                <span class="{text_color} text-sm font-bold">{percentage}%</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2">
                <div class="{bar_color} h-2 rounded-full" style="width: {percentage}%"></div>
            </div>
            <div class="text-xs text-gray-500 mt-1">{successes}/{attempts} attempts</div>
        </div>
        '''
    
    html += '</div>'
    return html

def _generate_failure_chart_html(failure_data):
    """Generate HTML for failure/caught rate chart"""
    if not failure_data:
        return '<p class="text-gray-500 text-center py-4">No data available for this session</p>'
    
    html = '<div class="space-y-3">'
    for i, data in enumerate(failure_data[:5]):  # Top 5
        percentage = data['caught_rate']
        attempts = data['attempts']
        caught = data['times_caught']
        
        # Color based on how often caught (red = bad, green = good defense)
        if percentage >= 80:
            bar_color = 'bg-red-500'
            text_color = 'text-red-700'
        elif percentage >= 60:
            bar_color = 'bg-orange-500'
            text_color = 'text-orange-700'
        elif percentage >= 40:
            bar_color = 'bg-yellow-500'
            text_color = 'text-yellow-700'
        else:
            bar_color = 'bg-green-500'
            text_color = 'text-green-700'
        
        html += f'''
        <div class="relative">
            <div class="flex justify-between items-center mb-1">
                <span class="text-sm font-medium truncate">{data['technique']}</span>
                <span class="{text_color} text-sm font-bold">{percentage}%</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2">
                <div class="{bar_color} h-2 rounded-full" style="width: {percentage}%"></div>
            </div>
            <div class="text-xs text-gray-500 mt-1">Caught {caught}/{attempts} times</div>
        </div>
        '''
    
    html += '</div>'
    return html

def _generate_all_techniques_html(techniques):
    """Generate HTML for all techniques overview"""
    if not techniques:
        return '<p class="text-gray-500 text-center py-8">No techniques detected in this video.</p>'
    
    html = f'''
    <div class="mb-6">
        <div class="text-lg text-gray-600 mb-4">Complete analysis of all {len(techniques)} detected techniques</div>
    </div>
    <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
                <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Technique</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Category</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Time</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Confidence</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Quality</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Rating</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Outcome</th>
                </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
    '''
    
    for tech in techniques:
        confidence_pct = tech.get('confidence', 0) * 100
        category_name = tech.get('category', '').replace('_', ' ').title()
        is_yours = tech.get('is_your_technique', True)
        outcome = tech.get('outcome', 'Unknown')
        
        # Color coding for outcome
        if is_yours:
            outcome_class = 'bg-green-100 text-green-800' if outcome == 'Success' else 'bg-yellow-100 text-yellow-800'
            outcome_text = f'Your {outcome}'
        else:
            outcome_class = 'bg-red-100 text-red-800' if outcome == 'Success' else 'bg-blue-100 text-blue-800'
            outcome_text = f'Opponent {outcome}'
        
        html += f'''
                <tr>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{tech.get('name', 'Unknown')}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{category_name}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{tech.get('start_time', 0):.1f}s</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{confidence_pct:.1f}%</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{tech.get('quality_score', 0):.1f}/100</td>
                    <td class="px-6 py-4 whitespace-nowrap">
                        <span class="bg-{_get_rating_color(tech.get('execution_rating', ''))} text-white text-xs px-2 py-1 rounded">
                            {tech.get('execution_rating', 'Unknown')}
                        </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                        <span class="{outcome_class} text-xs px-2 py-1 rounded">
                            {outcome_text}
                        </span>
                    </td>
                </tr>
        '''
    
    html += '''
            </tbody>
        </table>
    </div>
    '''
    return html

def _get_rating_color(rating):
    """Get Tailwind color class for execution rating"""
    rating_colors = {
        'Excellent': 'green-500',
        'Good': 'blue-500',
        'Fair': 'yellow-500',
        'Needs Work': 'red-500'
    }
    return rating_colors.get(rating, 'gray-500')

# Add these methods to the app for the HTML generation
app._generate_category_breakdown_html = _generate_category_breakdown_html
app._generate_insights_html = _generate_insights_html
app._generate_quality_metrics_html = _generate_quality_metrics_html
app._generate_technique_category_html = _generate_technique_category_html
app._generate_all_techniques_html = _generate_all_techniques_html
app._generate_success_chart_html = _generate_success_chart_html
app._generate_failure_chart_html = _generate_failure_chart_html
app._get_rating_color = _get_rating_color

# Initialize database on startup
try:
    init_database()
except Exception as e:
    logger.error(f"Database initialization failed: {str(e)}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)
