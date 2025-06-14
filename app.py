from flask import Flask, request, jsonify, session
import os
import json
import time
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'bjj-ai-secret-key-2024'

# Storage
users = {}
user_videos = {}
facebook_connections = {}

def get_user_id():
    if 'user_id' not in session:
        session['user_id'] = f"user_{random.randint(1000, 9999)}"
        users[session['user_id']] = {
            'plan': 'free',
            'videos_count': 0,
            'created_at': datetime.now().isoformat(),
            'monthly_uploads': 0,
            'last_upload_month': datetime.now().strftime('%Y-%m')
        }
        user_videos[session['user_id']] = []
    return session['user_id']

def generate_analysis(plan):
    techniques = []
    
    # Comprehensive technique list
    technique_list = [
        # Submissions
        {'name': 'armbar_from_guard', 'cat': 'submission'},
        {'name': 'triangle_choke', 'cat': 'submission'},
        {'name': 'rear_naked_choke', 'cat': 'submission'},
        {'name': 'kimura', 'cat': 'submission'},
        {'name': 'guillotine', 'cat': 'submission'},
        {'name': 'darce_choke', 'cat': 'submission'},
        {'name': 'omoplata', 'cat': 'submission'},
        {'name': 'americana', 'cat': 'submission'},
        {'name': 'heel_hook', 'cat': 'submission'},
        {'name': 'ankle_lock', 'cat': 'submission'},
        {'name': 'ezekiel_choke', 'cat': 'submission'},
        {'name': 'loop_choke', 'cat': 'submission'},
        {'name': 'bow_and_arrow_choke', 'cat': 'submission'},
        {'name': 'baseball_choke', 'cat': 'submission'},
        {'name': 'knee_bar', 'cat': 'submission'},
        {'name': 'toe_hold', 'cat': 'submission'},
        {'name': 'calf_slicer', 'cat': 'submission'},
        {'name': 'north_south_choke', 'cat': 'submission'},
        {'name': 'anaconda_choke', 'cat': 'submission'},
        {'name': 'peruvian_necktie', 'cat': 'submission'},
        
        # Sweeps
        {'name': 'scissor_sweep', 'cat': 'sweep'},
        {'name': 'butterfly_sweep', 'cat': 'sweep'},
        {'name': 'tripod_sweep', 'cat': 'sweep'},
        {'name': 'flower_sweep', 'cat': 'sweep'},
        {'name': 'hook_sweep', 'cat': 'sweep'},
        {'name': 'pendulum_sweep', 'cat': 'sweep'},
        {'name': 'spider_guard_sweep', 'cat': 'sweep'},
        {'name': 'de_la_riva_sweep', 'cat': 'sweep'},
        {'name': 'x_guard_sweep', 'cat': 'sweep'},
        {'name': 'berimbolo', 'cat': 'sweep'},
        {'name': 'old_school_sweep', 'cat': 'sweep'},
        {'name': 'hip_bump_sweep', 'cat': 'sweep'},
        {'name': 'sit_up_sweep', 'cat': 'sweep'},
        {'name': 'lasso_guard_sweep', 'cat': 'sweep'},
        {'name': 'balloon_sweep', 'cat': 'sweep'},
        {'name': 'tornado_sweep', 'cat': 'sweep'},
        {'name': 'knee_tap_sweep', 'cat': 'sweep'},
        {'name': 'electric_chair_sweep', 'cat': 'sweep'},
        
        # Guard Passes
        {'name': 'knee_cut_pass', 'cat': 'guard_pass'},
        {'name': 'toreando_pass', 'cat': 'guard_pass'},
        {'name': 'leg_drag', 'cat': 'guard_pass'},
        {'name': 'stack_pass', 'cat': 'guard_pass'},
        {'name': 'over_under_pass', 'cat': 'guard_pass'},
        {'name': 'x_pass', 'cat': 'guard_pass'},
        {'name': 'long_step_pass', 'cat': 'guard_pass'},
        {'name': 'smash_pass', 'cat': 'guard_pass'},
        {'name': 'headquarters_pass', 'cat': 'guard_pass'},
        {'name': 'knee_slide_pass', 'cat': 'guard_pass'},
        {'name': 'bullfighter_pass', 'cat': 'guard_pass'},
        {'name': 'cartwheel_pass', 'cat': 'guard_pass'},
        {'name': 'standing_pass', 'cat': 'guard_pass'},
        {'name': 'leg_weave_pass', 'cat': 'guard_pass'},
        
        # Takedowns
        {'name': 'double_leg_takedown', 'cat': 'takedown'},
        {'name': 'single_leg_takedown', 'cat': 'takedown'},
        {'name': 'hip_toss', 'cat': 'takedown'},
        {'name': 'foot_sweep', 'cat': 'takedown'},
        {'name': 'ankle_pick', 'cat': 'takedown'},
        {'name': 'duck_under', 'cat': 'takedown'},
        {'name': 'arm_drag_takedown', 'cat': 'takedown'},
        {'name': 'osoto_gari', 'cat': 'takedown'},
        {'name': 'seoi_nage', 'cat': 'takedown'},
        {'name': 'uchi_mata', 'cat': 'takedown'},
        {'name': 'high_crotch', 'cat': 'takedown'},
        {'name': 'fireman_carry', 'cat': 'takedown'},
        {'name': 'tai_otoshi', 'cat': 'takedown'},
        {'name': 'tomoe_nage', 'cat': 'takedown'},
        {'name': 'inside_trip', 'cat': 'takedown'},
        {'name': 'outside_trip', 'cat': 'takedown'},
        
        # Escapes
        {'name': 'mount_escape', 'cat': 'escape'},
        {'name': 'side_control_escape', 'cat': 'escape'},
        {'name': 'back_escape', 'cat': 'escape'},
        {'name': 'turtle_escape', 'cat': 'escape'},
        {'name': 'bridge_and_roll', 'cat': 'escape'},
        {'name': 'knee_on_belly_escape', 'cat': 'escape'},
        
        # Transitions
        {'name': 'guard_to_mount', 'cat': 'transition'},
        {'name': 'side_control_to_mount', 'cat': 'transition'},
        {'name': 'mount_to_back', 'cat': 'transition'},
        {'name': 'knee_on_belly_transition', 'cat': 'transition'},
        {'name': 'scramble', 'cat': 'transition'},
        
        # Guard Retention
        {'name': 'hip_escape', 'cat': 'guard_retention'},
        {'name': 'shrimping', 'cat': 'guard_retention'},
        {'name': 'knee_shield', 'cat': 'guard_retention'},
        {'name': 'frames', 'cat': 'guard_retention'},
        {'name': 'inversion', 'cat': 'guard_retention'}
    ]
    
    num_techniques = random.randint(8, 15)
    selected = random.sample(technique_list, min(num_techniques, len(technique_list)))
    
    for tech in selected:
        start_time = random.randint(10, 240)
        techniques.append({
            'technique': tech['name'],
            'category': tech['cat'],
            'confidence': round(random.uniform(0.75, 0.98), 2),
            'start_time': start_time,
            'end_time': start_time + random.randint(8, 20),
            'quality': random.choice(['excellent', 'good', 'fair']),
            'position': random.choice(['guard', 'mount', 'side_control', 'standing', 'half_guard', 'back_control', 'turtle', 'knee_on_belly']),
            'has_timestamp': (plan in ['pro', 'blackbelt']),
            'has_breakdown': (plan in ['pro', 'blackbelt'])
        })
    
    insights = [
        "🎯 Great technique diversity! You're showing skills across multiple categories.",
        "🔥 High execution quality detected in your submissions.",
        "🌊 Strong guard game - you're comfortable working from bottom.",
        "📈 Consistent performance across different positions.",
        "💪 Your timing on transitions is improving significantly.",
        "🎭 Developing a well-rounded game across all positions.",
        "🥋 Your defensive fundamentals are getting stronger.",
        "⚡ Quick transitions detected - great scrambling ability!",
        "🎪 Advanced techniques showing up - you're leveling up!",
        "🏆 Competition-ready techniques detected in your game.",
        "🛡️ Excellent escape timing - hard to hold down!",
        "🔄 Smooth position transitions - great flow!",
        "🎨 Creative technique combinations detected.",
        "📚 Textbook execution on fundamental techniques.",
        "🚀 Explosive movements - great athletic ability!"
    ]
    
    return {
        'total_techniques_detected': len(techniques),
        'detected_techniques': techniques,
        'video_duration': random.randint(180, 300),
        'techniques_per_minute': round(len(techniques) / 4, 1),
        'average_confidence': round(sum(t['confidence'] for t in techniques) / len(techniques), 2),
        'insights': random.sample(insights, 3),
        'analysis_timestamp': datetime.now().isoformat(),
        'user_plan': plan
    }

@app.route('/')
def home():
    user_id = get_user_id()
    
    # Ensure user exists
    if user_id not in users:
        users[user_id] = {
            'plan': 'free',
            'videos_count': 0,
            'created_at': datetime.now().isoformat(),
            'monthly_uploads': 0,
            'last_upload_month': datetime.now().strftime('%Y-%m'),
            'email': None,
            'name': None,
            'ai_learning_data': {
                'favorite_techniques': [],
                'weak_areas': [],
                'improvement_trends': [],
                'style_profile': 'balanced'
            }
        }
        user_videos[user_id] = []
    
    user = users[user_id]
    user_plan = user['plan']
    video_count = len(user_videos.get(user_id, []))
    
    # Check monthly upload limit
    current_month = datetime.now().strftime('%Y-%m')
    if user['last_upload_month'] != current_month:
        user['monthly_uploads'] = 0
        user['last_upload_month'] = current_month
    
    monthly_uploads = user['monthly_uploads']
    user_email = user.get('email', None)
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BJJ AI Analyzer Pro</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }}
        .glass {{ background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); }}
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}
        .tab-button.active {{ background: rgba(255, 255, 255, 0.2); }}
    </style>
</head>
<body class="min-h-screen">
    <!-- Header -->
    <div class="text-center py-8">
        <h1 class="text-5xl font-bold text-white mb-4">🥋 BJJ AI Analyzer Pro</h1>
        <p class="text-xl text-gray-200">Complete BJJ Analytics Platform</p>
        
        <!-- Login/Account Section -->
        {"" if user_email else '''
        <div class="mt-6 mb-4">
            <div class="bg-yellow-600 bg-opacity-20 rounded-lg p-4 max-w-md mx-auto border border-yellow-500">
                <h3 class="text-lg font-bold text-white mb-2">📧 Create Your Account</h3>
                <p class="text-yellow-100 text-sm mb-4">Save your progress & let AI learn your fighting style!</p>
                <div class="space-y-3">
                    <input type="email" id="userEmail" placeholder="Enter your email" 
                           class="w-full p-3 rounded-lg bg-white bg-opacity-20 text-white placeholder-gray-300">
                    <input type="text" id="userName" placeholder="Your name" 
                           class="w-full p-3 rounded-lg bg-white bg-opacity-20 text-white placeholder-gray-300">
                    <button onclick="createAccount()" class="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg font-bold w-full">
                        🚀 CREATE ACCOUNT & START TRACKING
                    </button>
                </div>
            </div>
        </div>'''}
        
        <div class="mt-4">
            <span class="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-lg text-lg font-bold">
                {user_plan.upper()} PLAN • {video_count} Videos Analyzed
                {"" if not user_email else f" • {user.get('name', 'User')}"}
            </span>
        </div>
        <div class="mt-4 space-x-4">
            <button onclick="showPricing()" class="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg font-bold text-lg">
                💎 UPGRADE NOW
            </button>
            {"" if user_plan != "free" else f'<span class="text-yellow-300 font-bold">Monthly Uploads: {monthly_uploads}/1</span>'}
            {"" if user_plan == "free" else f'<span class="text-green-300 font-bold">Monthly Uploads: {monthly_uploads}/{4 if user_plan == "pro" else "∞"}</span>'}
        </div>
    </div>

    <!-- Pricing Modal -->
    <div id="pricing-modal" class="fixed inset-0 bg-black bg-opacity-75 hidden z-50 flex items-center justify-center">
        <div class="glass rounded-2xl p-8 max-w-6xl mx-4">
            <div class="flex justify-between items-center mb-8">
                <h2 class="text-3xl font-bold text-white">Choose Your BJJ Journey</h2>
                <button onclick="hidePricing()" class="text-white text-3xl hover:text-red-400">&times;</button>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <!-- Free Plan -->
                <div class="bg-gray-800 bg-opacity-50 rounded-xl p-6 text-center border border-gray-600">
                    <h3 class="text-2xl font-bold text-white mb-4">🆓 Free</h3>
                    <div class="text-4xl font-bold text-white mb-6">$0<span class="text-lg">/month</span></div>
                    <ul class="text-gray-300 space-y-3 mb-8 text-left">
                        <li>✅ 1 upload per month</li>
                        <li>✅ Full technique percentages</li>
                        <li>✅ Basic analytics</li>
                        <li>❌ No breakdowns</li>
                        <li>❌ No timestamps</li>
                        <li>❌ No challenges</li>
                        <li>❌ No social features</li>
                    </ul>
                    <button onclick="selectPlan('free')" class="bg-gray-600 text-white py-3 px-6 rounded-lg w-full font-bold">
                        Current Plan
                    </button>
                </div>
                
                <!-- Pro Plan -->
                <div class="bg-blue-600 bg-opacity-30 rounded-xl p-6 text-center border-2 border-blue-400 transform scale-105">
                    <div class="bg-blue-500 text-white px-4 py-2 rounded-full text-sm mb-4">MOST POPULAR</div>
                    <h3 class="text-2xl font-bold text-white mb-4">🥋 Pro</h3>
                    <div class="text-4xl font-bold text-white mb-6">$29<span class="text-lg">/month</span></div>
                    <ul class="text-white space-y-3 mb-8 text-left">
                        <li>✅ 4 uploads per month</li>
                        <li>✅ Full technique percentages</li>
                        <li>✅ Detailed breakdowns</li>
                        <li>✅ Video timestamps</li>
                        <li>✅ Daily/Weekly challenges</li>
                        <li>✅ Facebook integration</li>
                        <li>✅ Friend challenges</li>
                    </ul>
                    <button onclick="selectPlan('pro')" class="bg-blue-600 hover:bg-blue-700 text-white py-3 px-8 rounded-lg w-full font-bold text-lg">
                        🚀 UPGRADE TO PRO
                    </button>
                </div>
                
                <!-- Black Belt Plan -->
                <div class="bg-black bg-opacity-50 rounded-xl p-6 text-center border-2 border-yellow-400">
                    <div class="bg-yellow-500 text-black px-4 py-2 rounded-full text-sm mb-4 font-bold">BLACK BELT</div>
                    <h3 class="text-2xl font-bold text-white mb-4">🥇 Black Belt</h3>
                    <div class="text-4xl font-bold text-white mb-6">$59<span class="text-lg">/month</span></div>
                    <ul class="text-yellow-100 space-y-3 mb-8 text-left">
                        <li>✅ UNLIMITED uploads</li>
                        <li>✅ Full technique percentages</li>
                        <li>✅ Advanced breakdowns</li>
                        <li>✅ Precise timestamps</li>
                        <li>✅ Daily/Weekly challenges</li>
                        <li>✅ Facebook integration</li>
                        <li>✅ Friend challenges</li>
                        <li>🔥 Competition analytics</li>
                        <li>🔥 Private coaching insights</li>
                        <li>🔥 3D movement analysis</li>
                        <li>🔥 AI training plans</li>
                        <li>🔥 Biomechanical scoring</li>
                        <li>🔥 Tournament prep tools</li>
                    </ul>
                    <button onclick="selectPlan('blackbelt')" class="bg-yellow-500 hover:bg-yellow-600 text-black py-3 px-8 rounded-lg w-full font-bold text-lg">
                        👑 GO BLACK BELT
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Navigation -->
    <div class="container mx-auto px-4 max-w-6xl mb-8">
        <div class="glass rounded-xl p-2">
            <div class="flex flex-wrap justify-center space-x-2">
                <button onclick="showTab('upload')" class="tab-button active px-6 py-3 rounded-lg text-white font-semibold text-lg">
                    📹 Upload
                </button>
                <button onclick="showTab('submissions')" class="tab-button px-6 py-3 rounded-lg text-white font-semibold text-lg">
                    🎯 Submissions
                </button>
                <button onclick="showTab('sweeps')" class="tab-button px-6 py-3 rounded-lg text-white font-semibold text-lg">
                    🌊 Sweeps
                </button>
                <button onclick="showTab('takedowns')" class="tab-button px-6 py-3 rounded-lg text-white font-semibold text-lg">
                    🤼 Takedowns
                </button>
                <button onclick="showTab('analytics')" class="tab-button px-6 py-3 rounded-lg text-white font-semibold text-lg">
                    📊 Analytics
                </button>
            </div>
        </div>
    </div>

    <div class="container mx-auto px-4 max-w-6xl">
        <!-- Upload Tab -->
        <div id="upload-tab" class="tab-content active">
            <div class="glass rounded-xl p-8">
                <h2 class="text-3xl font-bold text-white mb-8 text-center">Upload Your BJJ Video</h2>

                <div class="bg-gradient-to-r from-green-600 to-blue-600 rounded-xl p-8 text-center">
                    <h3 class="text-2xl font-bold text-white mb-4">🎥 Ready to Analyze Your Game?</h3>
                    <p class="text-white mb-6">Upload your training footage and get instant AI-powered technique analysis</p>
                    
                    <input type="file" id="videoFile" accept="video/*" class="mb-6 text-white bg-white bg-opacity-20 p-4 rounded-lg">
                    <br>
                    <button onclick="analyzeVideo()" class="bg-white text-blue-600 font-bold py-4 px-8 rounded-lg text-xl hover:bg-gray-100">
                        🤖 ANALYZE MY TECHNIQUES
                    </button>
                    
                    <div class="mt-6 text-white">
                        {"" if user_plan != "free" else f'<p>📊 Monthly uploads remaining: <strong>{1 - monthly_uploads}</strong></p>'}
                        {"" if user_plan == "free" else f'<p>📊 Monthly uploads: <strong>{monthly_uploads}/{4 if user_plan == "pro" else "∞"}</strong></p>'}
                    </div>
                </div>
            </div>

            <!-- Progress Section -->
            <div id="progress-section" class="glass rounded-xl p-8 mt-8 hidden">
                <h3 class="text-2xl font-bold text-white mb-6 text-center">🔍 AI Analyzing Your Techniques...</h3>
                <div class="w-full bg-gray-700 rounded-full h-6 mb-6">
                    <div id="progress-bar" class="bg-gradient-to-r from-green-500 to-blue-500 h-6 rounded-full transition-all duration-500" style="width: 0%"></div>
                </div>
                <p class="text-gray-300 text-center text-lg">🧠 Processing your BJJ footage with advanced AI...</p>
            </div>

            <!-- Results Section -->
            <div id="results-section" class="glass rounded-xl p-8 mt-8 hidden">
                <h3 class="text-3xl font-bold text-white mb-8 text-center">📊 Your BJJ Analysis</h3>
                
                <div class="grid grid-cols-2 md:grid-cols-4 gap-6 mb-8">
                    <div class="bg-gradient-to-br from-blue-500 to-blue-700 rounded-xl p-6 text-center">
                        <div class="text-3xl font-bold text-white" id="total-count">0</div>
                        <div class="text-blue-100">Techniques</div>
                    </div>
                    <div class="bg-gradient-to-br from-green-500 to-green-700 rounded-xl p-6 text-center">
                        <div class="text-3xl font-bold text-white" id="avg-confidence">0%</div>
                        <div class="text-green-100">Accuracy</div>
                    </div>
                    <div class="bg-gradient-to-br from-purple-500 to-purple-700 rounded-xl p-6 text-center">
                        <div class="text-3xl font-bold text-white" id="video-duration">0m</div>
                        <div class="text-purple-100">Duration</div>
                    </div>
                    <div class="bg-gradient-to-br from-red-500 to-red-700 rounded-xl p-6 text-center">
                        <div class="text-3xl font-bold text-white" id="submission-count">0</div>
                        <div class="text-red-100">Submissions</div>
                    </div>
                </div>

                <div id="techniques-list" class="space-y-4 mb-8"></div>
                
                <div class="bg-white bg-opacity-10 rounded-xl p-6">
                    <h4 class="text-2xl font-bold text-white mb-4">🧠 AI Insights</h4>
                    <div id="insights-list"></div>
                </div>
            </div>
        </div>

        <!-- Other tabs would go here -->
        <div id="submissions-tab" class="tab-content">
            <div class="glass rounded-xl p-8">
                <h2 class="text-3xl font-bold text-white mb-8 text-center">🎯 Submission Analysis</h2>
                <p class="text-white text-center">Upload videos to see your submission analytics!</p>
            </div>
        </div>

        <div id="sweeps-tab" class="tab-content">
            <div class="glass rounded-xl p-8">
                <h2 class="text-3xl font-bold text-white mb-8 text-center">🌊 Sweep Analysis</h2>
                <p class="text-white text-center">Upload videos to see your sweep analytics!</p>
            </div>
        </div>

        <div id="takedowns-tab" class="tab-content">
            <div class="glass rounded-xl p-8">
                <h2 class="text-3xl font-bold text-white mb-8 text-center">🤼 Takedown Analysis</h2>
                <p class="text-white text-center">Upload videos to see your takedown analytics!</p>
            </div>
        </div>

        <div id="analytics-tab" class="tab-content">
            <div class="glass rounded-xl p-8">
                <h2 class="text-3xl font-bold text-white mb-8 text-center">📊 Your BJJ Analytics</h2>
                <p class="text-white text-center">Upload videos to see detailed analytics!</p>
            </div>
        </div>
    </div>

    <script>
        const userPlan = "{user_plan}";
        const monthlyUploads = {monthly_uploads};
        const maxUploads = {1 if user_plan == "free" else (4 if user_plan == "pro" else 999)};
        const userEmail = "{user_email or ''}";

        function createAccount() {{
            var email = document.getElementById('userEmail').value.trim();
            var name = document.getElementById('userName').value.trim();
            
            if (!email || !name) {{
                alert('Please enter both email and name!');
                return;
            }}
            
            if (!email.includes('@')) {{
                alert('Please enter a valid email address!');
                return;
            }}
            
            fetch('/api/create-account', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{email: email, name: name}})
            }})
            .then(response => response.json())
            .then(data => {{
                if (data.success) {{
                    alert('🎉 Account created successfully!\\n\\nYour progress will now be saved and AI will learn your fighting style.');
                    location.reload();
                }} else {{
                    alert('❌ Error: ' + data.message);
                }}
            }})
            .catch(error => {{
                alert('Error creating account: ' + error.message);
            }});
        }}

        function showTab(tabName) {{
            document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
            document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
            document.getElementById(tabName + '-tab').classList.add('active');
            event.target.classList.add('active');
        }}

        function showPricing() {{
            document.getElementById('pricing-modal').classList.remove('hidden');
        }}

        function hidePricing() {{
            document.getElementById('pricing-modal').classList.add('hidden');
        }}

        function selectPlan(plan) {{
            if (plan === 'free') {{
                alert('You are already on the free plan!');
                return;
            }}
            
            const planNames = {{'pro': 'Pro ($29/month)', 'blackbelt': 'Black Belt ($59/month)'}};
            const confirmUpgrade = confirm(`Upgrade to ${{planNames[plan]}}?\\n\\nThis would redirect to PayPal in the real app.`);
            
            if (confirmUpgrade) {{
                alert(`🎉 Welcome to ${{planNames[plan]}}!\\n\\nYour account has been upgraded.`);
                location.reload();
            }}
        }}

        async function analyzeVideo() {{
            const fileInput = document.getElementById('videoFile');
            if (!fileInput.files[0]) {{
                alert('Please select a video file first!');
                return;
            }}

            // Check upload limits
            if (userPlan === 'free' && monthlyUploads >= 1) {{
                alert('Monthly upload limit reached!\\n\\nUpgrade to Pro for 4 uploads per month or Black Belt for unlimited uploads.');
                showPricing();
                return;
            }}
            
            if (userPlan === 'pro' && monthlyUploads >= 4) {{
                alert('Monthly upload limit reached!\\n\\nUpgrade to Black Belt for unlimited uploads.');
                showPricing();
                return;
            }}

            document.getElementById('progress-section').classList.remove('hidden');
            let progress = 0;
            const progressBar = document.getElementById('progress-bar');
            
            const interval = setInterval(() => {{
                progress += Math.random() * 12;
                if (progress > 100) progress = 100;
                progressBar.style.width = progress + '%';
                
                if (progress >= 100) {{
                    clearInterval(interval);
                    performAnalysis();
                }}
            }}, 400);
        }}

        async function performAnalysis() {{
            try {{
                const formData = new FormData();
                formData.append('video', document.getElementById('videoFile').files[0]);

                const response = await fetch('/api/analyze', {{
                    method: 'POST',
                    body: formData
                }});

                const results = await response.json();
                
                if (results.error) {{
                    alert('❌ ' + results.error);
                    document.getElementById('progress-section').classList.add('hidden');
                    return;
                }}
                
                displayResults(results);
            }} catch (error) {{
                alert('Analysis failed: ' + error.message);
                document.getElementById('progress-section').classList.add('hidden');
            }}
        }}

        function displayResults(results) {{
            document.getElementById('progress-section').classList.add('hidden');
            document.getElementById('results-section').classList.remove('hidden');

            document.getElementById('total-count').textContent = results.total_techniques_detected || 0;
            document.getElementById('avg-confidence').textContent = Math.round((results.average_confidence || 0) * 100) + '%';
            document.getElementById('video-duration').textContent = Math.round((results.video_duration || 0) / 60) + 'm';
            
            const submissionCount = (results.detected_techniques || []).filter(t => t.category === 'submission').length;
            document.getElementById('submission-count').textContent = submissionCount;

            displayTechniques(results.detected_techniques || []);
            displayInsights(results.insights || []);
        }}

        function displayTechniques(techniques) {{
            const techniquesList = document.getElementById('techniques-list');
            techniquesList.innerHTML = '';

            techniques.forEach(technique => {{
                const techniqueDiv = document.createElement('div');
                techniqueDiv.className = 'bg-white bg-opacity-10 rounded-xl p-6 border-l-4 border-blue-500';
                
                let timestampHTML = '';
                if (technique.has_timestamp) {{
                    timestampHTML = `
                        <button onclick="alert('🎬 Timestamp: ${{Math.floor(technique.start_time/60)}}:${{(technique.start_time%60).toString().padStart(2, '0')}}')" 
                                class="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-sm ml-3">
                            🎬 ${{Math.floor(technique.start_time/60)}}:${{(technique.start_time%60).toString().padStart(2, '0')}}
                        </button>
                    `;
                }}

                let breakdownHTML = '';
                if (technique.has_breakdown) {{
                    breakdownHTML = `
                        <button onclick="alert('📋 Full breakdown available for ${{technique.technique.replace(/_/g, ' ')}}!')" 
                                class="bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded text-sm ml-2">
                            📋 Breakdown
                        </button>
                    `;
                }}

                techniqueDiv.innerHTML = `
                    <div class="flex justify-between items-center">
                        <div class="flex-1">
                            <div class="flex items-center mb-2">
                                <h4 class="text-xl font-bold text-white">${{technique.technique.replace(/_/g, ' ').replace(/\\b\\w/g, l => l.toUpperCase())}}</h4>
                                <span class="ml-3 px-3 py-1 bg-blue-600 rounded-full text-xs text-white">
                                    ${{technique.category.replace('_', ' ').toUpperCase()}}
                                </span>
                                ${{timestampHTML}}
                                ${{breakdownHTML}}
                            </div>
                            <p class="text-gray-300">Position: ${{technique.position}} • Quality: ${{technique.quality}}</p>
                        </div>
                        <div class="text-right">
                            <div class="text-2xl font-bold text-white">${{Math.round(technique.confidence * 100)}}%</div>
                            <div class="text-gray-300 text-sm">Confidence</div>
                        </div>
                    </div>
                `;
                
                techniquesList.appendChild(techniqueDiv);
            }});
        }}

        function displayInsights(insights) {{
            const insightsList = document.getElementById('insights-list');
            insightsList.innerHTML = '';

            insights.forEach(insight => {{
                const insightDiv = document.createElement('div');
                insightDiv.className = 'bg-white bg-opacity-10 rounded-lg p-4 mb-3';
                insightDiv.innerHTML = `<p class="text-white text-lg">${{insight}}</p>`;
                insightsList.appendChild(insightDiv);
            }});
        }}
    </script>
</body>
</html>'''

@app.route('/api/create-account', methods=['POST'])
def create_account():
    user_id = get_user_id()
    data = request.get_json()
    email = data.get('email', '').strip()
    name = data.get('name', '').strip()
    
    if not email or not name:
        return jsonify({'success': False, 'message': 'Email and name are required'}), 400
    
    if '@' not in email:
        return jsonify({'success': False, 'message': 'Please enter a valid email'}), 400
    
    # Update user with account info
    if user_id in users:
        users[user_id]['email'] = email
        users[user_id]['name'] = name
        users[user_id]['account_created'] = datetime.now().isoformat()
        return jsonify({'success': True, 'message': 'Account created successfully!'})
    else:
        return jsonify({'success': False, 'message': 'User session not found'}), 400

@app.route('/api/analyze', methods=['POST'])
def analyze():
    user_id = get_user_id()
    
    # Ensure user exists
    if user_id not in users:
        return jsonify({'error': 'User session not found'}), 400
        
    user = users[user_id]
    user_plan = user['plan']
    
    # Check monthly upload limits
    current_month = datetime.now().strftime('%Y-%m')
    if user['last_upload_month'] != current_month:
        user['monthly_uploads'] = 0
        user['last_upload_month'] = current_month
    
    if user_plan == 'free' and user['monthly_uploads'] >= 1:
        return jsonify({'error': 'Monthly upload limit reached! Upgrade to Pro for 4 uploads per month.'}), 403
    
    if user_plan == 'pro' and user['monthly_uploads'] >= 4:
        return jsonify({'error': 'Monthly upload limit reached! Upgrade to Black Belt for unlimited uploads.'}), 403
    
    # Simulate processing time
    time.sleep(2)
    
    # Generate analysis
    analysis_result = generate_analysis(user_plan)
    
    # Store the analysis
    if user_id not in user_videos:
        user_videos[user_id] = []
    user_videos[user_id].append(analysis_result)
    
    # Update counters
    user['monthly_uploads'] += 1
    users[user_id]['videos_count'] += 1
    
    return jsonify(analysis_result)

@app.route('/api/upgrade', methods=['POST'])
def upgrade():
    user_id = get_user_id()
    data = request.get_json()
    new_plan = data.get('plan')
    
    if new_plan in ['pro', 'blackbelt']:
        users[user_id]['plan'] = new_plan
        return jsonify({'success': True, 'message': f'Successfully upgraded to {new_plan}!'})
    else:
        return jsonify({'success': False, 'message': 'Invalid plan'}), 400

@app.route('/health')
def health():
    return jsonify({'status': 'running', 'message': 'BJJ AI Analyzer Pro is ready!'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
