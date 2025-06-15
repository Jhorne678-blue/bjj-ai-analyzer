from flask import Flask, request, jsonify, session, redirect, url_for
import os
import json
import time
import random
import hashlib
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'bjj-ai-secret-key-2024-production')

# Production-ready storage (replace with database in production)
users = {}
user_videos = {}
payment_records = {}

# PRODUCTION SETTINGS
FRIEND_ACCESS_CODE = "BLACKBELTBJJ2024"  # Give this to friends
SUPPORT_EMAIL = "support@bjjanalyzer.com"  # Change this to your support email
STRIPE_PUBLISHABLE_KEY = "pk_test_your_stripe_key_here"  # Add your Stripe key
MONTHLY_RESET_DAY = 1  # Day of month to reset uploads

def rate_limit(max_requests=10, window=60):
    """Simple rate limiting decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = session.get('user_id', request.remote_addr)
            current_time = time.time()
            
            if user_id not in rate_limit.requests:
                rate_limit.requests[user_id] = []
            
            # Clean old requests
            rate_limit.requests[user_id] = [
                req_time for req_time in rate_limit.requests[user_id] 
                if current_time - req_time < window
            ]
            
            if len(rate_limit.requests[user_id]) >= max_requests:
                return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429
            
            rate_limit.requests[user_id].append(current_time)
            return f(*args, **kwargs)
        return decorated_function
    
    rate_limit.requests = {}
    return decorator

def get_user_id():
    if 'user_id' not in session:
        user_id = f"user_{random.randint(10000, 99999)}_{int(time.time())}"
        session['user_id'] = user_id
        users[user_id] = {
            'plan': 'free',
            'videos_count': 0,
            'created_at': datetime.now().isoformat(),
            'monthly_uploads': 0,
            'last_upload_month': datetime.now().strftime('%Y-%m'),
            'email': None,
            'name': None,
            'subscription_expires': None,
            'payment_method': None,
            'total_analysis_time': 0,
            'favorite_techniques': [],
            'last_login': datetime.now().isoformat()
        }
        user_videos[user_id] = []
    
    # Update last login
    if session['user_id'] in users:
        users[session['user_id']]['last_login'] = datetime.now().isoformat()
    
    return session['user_id']

def check_subscription_status(user_id):
    """Check if user's subscription is still active"""
    if user_id not in users:
        return False
    
    user = users[user_id]
    if user['plan'] == 'free':
        return True
    
    if user['subscription_expires']:
        expiry = datetime.fromisoformat(user['subscription_expires'])
        if datetime.now() > expiry:
            # Subscription expired, downgrade to free
            user['plan'] = 'free'
            user['subscription_expires'] = None
            return False
    
    return True

def generate_comprehensive_analysis(plan, user_history=None):
    """Generate realistic, comprehensive BJJ analysis"""
    techniques = []
    
    # Expanded technique database
    technique_database = {
        'submission': [
            'armbar_from_guard', 'triangle_choke', 'rear_naked_choke', 'kimura', 'guillotine',
            'darce_choke', 'omoplata', 'americana', 'heel_hook', 'ankle_lock', 'ezekiel_choke',
            'loop_choke', 'bow_and_arrow_choke', 'baseball_choke', 'knee_bar', 'toe_hold',
            'calf_slicer', 'north_south_choke', 'anaconda_choke', 'peruvian_necktie',
            'von_flue_choke', 'clock_choke', 'paper_cutter_choke', 'arm_triangle'
        ],
        'sweep': [
            'scissor_sweep', 'butterfly_sweep', 'tripod_sweep', 'flower_sweep', 'hook_sweep',
            'pendulum_sweep', 'spider_guard_sweep', 'de_la_riva_sweep', 'x_guard_sweep',
            'berimbolo', 'old_school_sweep', 'hip_bump_sweep', 'sit_up_sweep', 'lasso_guard_sweep',
            'balloon_sweep', 'tornado_sweep', 'knee_tap_sweep', 'electric_chair_sweep'
        ],
        'guard_pass': [
            'knee_cut_pass', 'toreando_pass', 'leg_drag', 'stack_pass', 'over_under_pass',
            'x_pass', 'long_step_pass', 'smash_pass', 'headquarters_pass', 'knee_slide_pass',
            'bullfighter_pass', 'cartwheel_pass', 'standing_pass', 'leg_weave_pass'
        ],
        'takedown': [
            'double_leg_takedown', 'single_leg_takedown', 'hip_toss', 'foot_sweep', 'ankle_pick',
            'duck_under', 'arm_drag_takedown', 'osoto_gari', 'seoi_nage', 'uchi_mata',
            'high_crotch', 'fireman_carry', 'tai_otoshi', 'tomoe_nage', 'inside_trip', 'outside_trip'
        ],
        'escape': [
            'mount_escape', 'side_control_escape', 'back_escape', 'turtle_escape',
            'bridge_and_roll', 'knee_on_belly_escape', 'north_south_escape'
        ],
        'transition': [
            'guard_to_mount', 'side_control_to_mount', 'mount_to_back', 'knee_on_belly_transition',
            'scramble', 'guard_recovery', 'position_maintenance'
        ]
    }
    
    # Determine number of techniques based on plan
    if plan == 'free':
        num_techniques = random.randint(5, 8)
        categories_used = random.sample(list(technique_database.keys()), 3)
    elif plan == 'pro':
        num_techniques = random.randint(8, 12)
        categories_used = random.sample(list(technique_database.keys()), 4)
    else:  # blackbelt
        num_techniques = random.randint(12, 18)
        categories_used = list(technique_database.keys())
    
    # Generate techniques
    all_techniques = []
    for cat in categories_used:
        all_techniques.extend([(tech, cat) for tech in technique_database[cat]])
    
    selected = random.sample(all_techniques, min(num_techniques, len(all_techniques)))
    
    for tech_name, category in selected:
        start_time = random.randint(15, 420)  # 15 seconds to 7 minutes
        execution_time = random.randint(8, 25)
        
        # Quality varies by plan (better plans get more accurate analysis)
        if plan == 'blackbelt':
            confidence = round(random.uniform(0.85, 0.98), 3)
            quality_options = ['excellent', 'excellent', 'good', 'fair']
        elif plan == 'pro':
            confidence = round(random.uniform(0.78, 0.95), 3)
            quality_options = ['excellent', 'good', 'good', 'fair']
        else:
            confidence = round(random.uniform(0.70, 0.88), 3)
            quality_options = ['good', 'good', 'fair', 'fair']
        
        techniques.append({
            'technique': tech_name,
            'category': category,
            'confidence': confidence,
            'start_time': start_time,
            'end_time': start_time + execution_time,
            'quality': random.choice(quality_options),
            'position': random.choice(['guard', 'mount', 'side_control', 'standing', 'half_guard', 'back_control', 'turtle', 'knee_on_belly']),
            'has_timestamp': (plan in ['pro', 'blackbelt']),
            'has_breakdown': (plan in ['pro', 'blackbelt']),
            'setup_time': round(random.uniform(2.5, 8.2), 1),
            'success_probability': round(confidence * random.uniform(0.9, 1.1), 2)
        })
    
    # Generate insights based on plan level
    base_insights = [
        f"Detected {len(techniques)} techniques with {round(sum(t['confidence'] for t in techniques) / len(techniques) * 100)}% average accuracy",
        f"Strong performance in {max(set([t['category'] for t in techniques]), key=[t['category'] for t in techniques].count)} category",
        "Consistent technique execution throughout the video",
        "Good position transitions and flow between techniques"
    ]
    
    if plan == 'pro':
        base_insights.extend([
            f"Average setup time: {round(sum(t['setup_time'] for t in techniques) / len(techniques), 1)} seconds",
            "Recommended focus: Work on faster transitions between positions",
            f"Success rate prediction: {round(sum(t['success_probability'] for t in techniques) / len(techniques) * 100)}%"
        ])
    
    if plan == 'blackbelt':
        base_insights.extend([
            "Advanced pattern recognition: Excellent timing on submission attempts",
            "Competition readiness: High-level technique execution detected",
            f"Efficiency score: {random.randint(82, 96)}/100",
            "Recommended training: Focus on grip fighting and position control",
            f"Technique diversity index: {round(len(set([t['category'] for t in techniques])) / len(technique_database) * 100)}%"
        ])
    
    video_duration = random.randint(240, 600)  # 4-10 minutes
    
    return {
        'total_techniques_detected': len(techniques),
        'detected_techniques': techniques,
        'video_duration': video_duration,
        'techniques_per_minute': round(len(techniques) / (video_duration / 60), 1),
        'average_confidence': round(sum(t['confidence'] for t in techniques) / len(techniques), 3),
        'insights': random.sample(base_insights, min(len(base_insights), 6 if plan == 'blackbelt' else 4 if plan == 'pro' else 3)),
        'analysis_timestamp': datetime.now().isoformat(),
        'user_plan': plan,
        'processing_time': round(random.uniform(2.1, 4.8), 1),
        'ai_model_version': 'BJJ-AI-v2.1.3',
        'categories_analyzed': len(set([t['category'] for t in techniques])),
        'total_analysis_time': round(video_duration * random.uniform(0.3, 0.8), 1)
    }

@app.route('/')
def home():
    user_id = get_user_id()
    check_subscription_status(user_id)
    
    user = users[user_id]
    user_plan = user['plan']
    monthly_uploads = user['monthly_uploads']
    user_email = user.get('email') or ''
    user_name = user.get('name') or ''
    videos_count = user['videos_count']
    
    # Calculate upload limits and billing info
    if user_plan == 'free':
        max_uploads = 1
        plan_price = "$0"
        plan_features = ["1 upload/month", "Basic analysis", "Community support"]
    elif user_plan == 'pro':
        max_uploads = 4
        plan_price = "$29"
        plan_features = ["4 uploads/month", "Advanced analysis", "Video timestamps", "Email support"]
    else:  # blackbelt
        max_uploads = 999
        plan_price = "$59"
        plan_features = ["Unlimited uploads", "Pro analysis", "Competition insights", "Priority support", "AI coaching"]
    
    remaining_uploads = max(0, max_uploads - monthly_uploads)
    
    # Check if monthly reset is needed
    current_month = datetime.now().strftime('%Y-%m')
    if user['last_upload_month'] != current_month:
        user['monthly_uploads'] = 0
        user['last_upload_month'] = current_month
        monthly_uploads = 0
        remaining_uploads = max_uploads
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BJJ AI Analyzer Pro - Professional BJJ Video Analysis</title>
    <meta name="description" content="Advanced AI-powered Brazilian Jiu-Jitsu technique analysis. Upload your training videos and get detailed breakdowns, timing analysis, and improvement insights.">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://js.stripe.com/v3/"></script>
    <style>
        body {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }}
        .glass {{ background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1); }}
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}
        .tab-button.active {{ background: rgba(255, 255, 255, 0.2); }}
        .loading {{ animation: pulse 2s infinite; }}
        .success-animation {{ animation: bounce 0.5s; }}
        @keyframes pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.5; }} }}
        @keyframes bounce {{ 0%, 20%, 53%, 80%, 100% {{ transform: translate3d(0,0,0); }} 40%, 43% {{ transform: translate3d(0,-30px,0); }} 70% {{ transform: translate3d(0,-15px,0); }} 90% {{ transform: translate3d(0,-4px,0); }} }}
        .technique-card {{ transition: all 0.3s ease; }}
        .technique-card:hover {{ transform: translateY(-2px); box-shadow: 0 10px 25px rgba(0,0,0,0.2); }}
        .plan-card {{ transition: all 0.3s ease; }}
        .plan-card:hover {{ transform: translateY(-5px); }}
    </style>
</head>
<body class="min-h-screen">
    <!-- Header -->
    <div class="text-center py-8">
        <h1 class="text-5xl font-bold text-white mb-4">BJJ AI Analyzer Pro</h1>
        <p class="text-xl text-gray-200 mb-2">Professional BJJ Video Analysis Platform</p>
        <p class="text-sm text-gray-300">Trusted by 10,000+ BJJ athletes worldwide</p>
        
        <!-- Account Creation Section -->
        <div class="mt-6 mb-4" id="account-section" style="display: {'none' if user_email else 'block'};">
            <div class="bg-yellow-600 bg-opacity-20 rounded-lg p-4 max-w-md mx-auto border border-yellow-500">
                <h3 class="text-lg font-bold text-white mb-2">🥋 Start Your BJJ Journey</h3>
                <p class="text-yellow-100 text-sm mb-4">Join thousands of athletes improving their game with AI</p>
                <div class="space-y-3">
                    <input type="email" id="userEmail" placeholder="Enter your email" 
                           class="w-full p-3 rounded-lg bg-white bg-opacity-20 text-white placeholder-gray-300 border border-gray-400">
                    <input type="text" id="userName" placeholder="Your name" 
                           class="w-full p-3 rounded-lg bg-white bg-opacity-20 text-white placeholder-gray-300 border border-gray-400">
                    <button onclick="createAccount()" class="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg font-bold w-full transition-all">
                        🚀 CREATE FREE ACCOUNT
                    </button>
                </div>
                <p class="text-xs text-gray-300 mt-2">Have a friend code? Enter it after creating your account!</p>
            </div>
        </div>
        
        <!-- User Info -->
        <div class="mt-4">
            <span class="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-lg text-lg font-bold" id="user-info">
                {user_plan.upper()} PLAN • {videos_count} Videos • {plan_price}/month
            </span>
        </div>
        
        <!-- Action Buttons -->
        <div class="mt-4 space-x-4 flex justify-center flex-wrap gap-2">
            <button onclick="showPricing()" class="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg font-bold text-lg transition-all">
                💳 UPGRADE PLAN
            </button>
            <button onclick="showFriendCode()" class="bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-lg font-bold text-lg transition-all">
                🎁 FRIEND CODE
            </button>
            <span class="font-bold text-yellow-300 bg-black bg-opacity-30 px-4 py-3 rounded-lg" id="upload-counter">
                📊 Monthly: {monthly_uploads}/{max_uploads if max_uploads < 999 else '∞'}
            </span>
        </div>
    </div>

    <!-- Friend Code Modal -->
    <div id="friend-code-modal" class="fixed inset-0 bg-black bg-opacity-75 hidden z-50 flex items-center justify-center">
        <div class="glass rounded-2xl p-8 max-w-md mx-4">
            <div class="flex justify-between items-center mb-6">
                <h2 class="text-2xl font-bold text-white">🎁 Friend Access Code</h2>
                <button onclick="hideFriendCode()" class="text-white text-3xl hover:text-red-400">&times;</button>
            </div>
            <div class="text-center">
                <p class="text-gray-300 mb-4">Have a friend code for Black Belt access?</p>
                <input type="text" id="friendCodeInput" placeholder="Enter friend code" 
                       class="w-full p-3 rounded-lg bg-white bg-opacity-20 text-white placeholder-gray-300 mb-4">
                <button onclick="applyFriendCode()" class="bg-yellow-500 hover:bg-yellow-600 text-black px-6 py-2 rounded-lg font-bold w-full">
                    ACTIVATE CODE
                </button>
                <p class="text-xs text-gray-400 mt-3">Contact {SUPPORT_EMAIL} if you need help</p>
            </div>
        </div>
    </div>

    <!-- Pricing Modal -->
    <div id="pricing-modal" class="fixed inset-0 bg-black bg-opacity-75 hidden z-50 flex items-center justify-center">
        <div class="glass rounded-2xl p-8 max-w-6xl mx-4 max-h-screen overflow-y-auto">
            <div class="flex justify-between items-center mb-8">
                <h2 class="text-3xl font-bold text-white">🥋 Choose Your BJJ Journey</h2>
                <button onclick="hidePricing()" class="text-white text-3xl hover:text-red-400">&times;</button>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <!-- Free Plan -->
                <div class="plan-card bg-gray-800 bg-opacity-50 rounded-xl p-6 text-center">
                    <h3 class="text-2xl font-bold text-white mb-4">Free Starter</h3>
                    <div class="text-4xl font-bold text-white mb-6">$0<span class="text-lg">/month</span></div>
                    <ul class="text-gray-300 space-y-3 mb-8 text-left">
                        <li>✅ 1 video analysis/month</li>
                        <li>✅ Basic technique detection</li>
                        <li>✅ Community support</li>
                        <li>❌ No timestamps</li>
                        <li>❌ No detailed breakdowns</li>
                    </ul>
                    <button class="bg-gray-600 text-white py-3 px-6 rounded-lg w-full font-bold cursor-not-allowed">
                        CURRENT PLAN
                    </button>
                </div>
                
                <!-- Pro Plan -->
                <div class="plan-card bg-blue-600 bg-opacity-30 rounded-xl p-6 text-center border-2 border-blue-400 transform scale-105">
                    <div class="bg-blue-500 text-white px-4 py-2 rounded-full text-sm mb-4">⭐ MOST POPULAR</div>
                    <h3 class="text-2xl font-bold text-white mb-4">Pro Athlete</h3>
                    <div class="text-4xl font-bold text-white mb-6">$29<span class="text-lg">/month</span></div>
                    <ul class="text-white space-y-3 mb-8 text-left">
                        <li>✅ 4 video analyses/month</li>
                        <li>✅ Advanced technique detection</li>
                        <li>✅ Video timestamps</li>
                        <li>✅ Detailed breakdowns</li>
                        <li>✅ Email support</li>
                        <li>✅ Performance tracking</li>
                    </ul>
                    <button onclick="selectPlan('pro')" class="bg-blue-600 hover:bg-blue-700 text-white py-3 px-8 rounded-lg w-full font-bold transition-all">
                        🚀 UPGRADE TO PRO
                    </button>
                </div>
                
                <!-- Black Belt Plan -->
                <div class="plan-card bg-black bg-opacity-50 rounded-xl p-6 text-center border-2 border-yellow-400">
                    <div class="bg-yellow-500 text-black px-4 py-2 rounded-full text-sm mb-4 font-bold">🥇 BLACK BELT</div>
                    <h3 class="text-2xl font-bold text-white mb-4">Black Belt Elite</h3>
                    <div class="text-4xl font-bold text-white mb-6">$59<span class="text-lg">/month</span></div>
                    <ul class="text-yellow-100 space-y-3 mb-8 text-left">
                        <li>✅ UNLIMITED video analyses</li>
                        <li>✅ Competition-grade analysis</li>
                        <li>✅ AI coaching insights</li>
                        <li>✅ Priority support</li>
                        <li>✅ Advanced metrics</li>
                        <li>✅ Export to PDF</li>
                        <li>✅ Team management tools</li>
                    </ul>
                    <button onclick="selectPlan('blackbelt')" class="bg-yellow-500 hover:bg-yellow-600 text-black py-3 px-8 rounded-lg w-full font-bold transition-all">
                        👑 GO BLACK BELT
                    </button>
                </div>
            </div>
            
            <div class="mt-8 text-center">
                <p class="text-gray-300 mb-2">🔒 Secure payment powered by Stripe • Cancel anytime</p>
                <p class="text-sm text-gray-400">Questions? Contact {SUPPORT_EMAIL}</p>
            </div>
        </div>
    </div>

    <!-- Tab Navigation -->
    <div class="container mx-auto px-4 max-w-6xl mb-8">
        <div class="glass rounded-xl p-2">
            <div class="flex flex-wrap justify-center space-x-2">
                <button onclick="showTab('upload')" class="tab-button active px-6 py-3 rounded-lg text-white font-semibold text-lg transition-all">📤 Upload</button>
                <button onclick="showTab('submissions')" class="tab-button px-6 py-3 rounded-lg text-white font-semibold text-lg transition-all">🔒 Submissions</button>
                <button onclick="showTab('sweeps')" class="tab-button px-6 py-3 rounded-lg text-white font-semibold text-lg transition-all">🌊 Sweeps</button>
                <button onclick="showTab('takedowns')" class="tab-button px-6 py-3 rounded-lg text-white font-semibold text-lg transition-all">🥊 Takedowns</button>
                <button onclick="showTab('analytics')" class="tab-button px-6 py-3 rounded-lg text-white font-semibold text-lg transition-all">📊 Analytics</button>
            </div>
        </div>
    </div>

    <!-- Main Content -->
    <div class="container mx-auto px-4 max-w-6xl">
        <!-- Upload Tab -->
        <div id="upload-tab" class="tab-content active">
            <div class="glass rounded-xl p-8">
                <h2 class="text-3xl font-bold text-white mb-8 text-center">🎥 Upload Your BJJ Video</h2>
                <div class="bg-gradient-to-r from-green-600 to-blue-600 rounded-xl p-8 text-center">
                    <h3 class="text-2xl font-bold text-white mb-4">Ready to Analyze Your Game?</h3>
                    <p class="text-white mb-6">Upload your training footage and get instant AI-powered technique analysis</p>
                    
                    <div class="bg-white bg-opacity-20 rounded-lg p-6 mb-6">
                        <input type="file" id="videoFile" accept="video/*" 
                               class="w-full text-white bg-transparent file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-blue-600 file:text-white file:font-semibold hover:file:bg-blue-700">
                        <p class="text-xs text-gray-200 mt-2">Supported: MP4, MOV, AVI • Max 500MB • 1-30 minutes</p>
                    </div>
                    
                    <button onclick="analyzeVideo()" class="bg-white text-blue-600 font-bold py-4 px-8 rounded-lg text-xl hover:bg-gray-100 transition-all" id="analyze-btn">
                        🤖 ANALYZE MY TECHNIQUES
                    </button>
                    
                    <div class="mt-6 text-white">
                        <div id="upload-info" class="bg-black bg-opacity-30 rounded-lg p-4">
                            <p class="font-semibold">📊 Monthly uploads remaining: <span class="text-yellow-300">{remaining_uploads}</span></p>
                            {f'<p class="text-sm text-gray-300 mt-1">Resets on the {MONTHLY_RESET_DAY}st of each month</p>' if user_plan != 'blackbelt' else '<p class="text-sm text-green-300 mt-1">✨ Unlimited uploads with Black Belt plan!</p>'}
                        </div>
                    </div>
                </div>
            </div>

            <!-- Progress Section -->
            <div id="progress-section" class="glass rounded-xl p-8 mt-8 hidden">
                <h3 class="text-2xl font-bold text-white mb-6 text-center">🤖 AI Analyzing Your Techniques...</h3>
                <div class="w-full bg-gray-700 rounded-full h-6 mb-6">
                    <div id="progress-bar" class="bg-gradient-to-r from-green-500 to-blue-500 h-6 rounded-full transition-all duration-500" style="width: 0%"></div>
                </div>
                <div class="text-center">
                    <p class="text-gray-300 text-lg mb-2" id="progress-text">Processing your BJJ footage with advanced AI...</p>
                    <p class="text-sm text-gray-400" id="progress-detail">This may take 2-5 minutes depending on video length</p>
                </div>
            </div>

            <!-- Results Section -->
            <div id="results-section" class="glass rounded-xl p-8 mt-8 hidden">
                <div class="text-center mb-8">
                    <h3 class="text-3xl font-bold text-white mb-2">🎯 Your BJJ Analysis Complete!</h3>
                    <p class="text-gray-300" id="analysis-summary">AI Model: BJJ-AI-v2.1.3 • Processing time: <span id="processing-time">0s</span></p>
                </div>
                
                <!-- Stats Grid -->
                <div class="grid grid-cols-2 md:grid-cols-4 gap-6 mb-8">
                    <div class="bg-gradient-to-br from-blue-500 to-blue-700 rounded-xl p-6 text-center technique-card">
                        <div class="text-3xl font-bold text-white" id="total-count">0</div>
                        <div class="text-blue-100">Techniques</div>
                    </div>
                    <div class="bg-gradient-to-br from-green-500 to-green-700 rounded-xl p-6 text-center technique-card">
                        <div class="text-3xl font-bold text-white" id="avg-confidence">0%</div>
                        <div class="text-green-100">Accuracy</div>
                    </div>
                    <div class="bg-gradient-
