from flask import Flask, request, jsonify, session
import os
import json
import time
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'bjj-ai-secret-key-2024'

# Global storage
users = {}
user_videos = {}

def get_user_id():
    if 'user_id' not in session:
        session['user_id'] = f"user_{random.randint(1000, 9999)}"
        users[session['user_id']] = {
            'plan': 'free',
            'videos_count': 0,
            'created_at': datetime.now().isoformat(),
            'monthly_uploads': 0,
            'last_upload_month': datetime.now().strftime('%Y-%m'),
            'email': None,
            'name': None
        }
        user_videos[session['user_id']] = []
    return session['user_id']

def generate_analysis(plan):
    techniques = []
    technique_list = [
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
        {'name': 'mount_escape', 'cat': 'escape'},
        {'name': 'side_control_escape', 'cat': 'escape'},
        {'name': 'back_escape', 'cat': 'escape'},
        {'name': 'turtle_escape', 'cat': 'escape'},
        {'name': 'bridge_and_roll', 'cat': 'escape'},
        {'name': 'knee_on_belly_escape', 'cat': 'escape'},
        {'name': 'guard_to_mount', 'cat': 'transition'},
        {'name': 'side_control_to_mount', 'cat': 'transition'},
        {'name': 'mount_to_back', 'cat': 'transition'},
        {'name': 'knee_on_belly_transition', 'cat': 'transition'},
        {'name': 'scramble', 'cat': 'transition'},
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
            'position': random.choice(['guard', 'mount', 'side_control', 'standing', 'half_guard', 'back_control']),
            'has_timestamp': (plan in ['pro', 'blackbelt']),
            'has_breakdown': (plan in ['pro', 'blackbelt'])
        })
    
    insights = [
        "Great technique diversity! You're showing skills across multiple categories.",
        "High execution quality detected in your submissions.",
        "Strong guard game - you're comfortable working from bottom.",
        "Consistent performance across different positions.",
        "Your timing on transitions is improving significantly.",
        "Developing a well-rounded game across all positions."
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
    
    # Ensure user exists in dictionary
    if user_id not in users:
        users[user_id] = {
            'plan': 'free',
            'videos_count': 0,
            'created_at': datetime.now().isoformat(),
            'monthly_uploads': 0,
            'last_upload_month': datetime.now().strftime('%Y-%m'),
            'email': None,
            'name': None
        }
        user_videos[user_id] = []
    
    user = users[user_id]
    
    # Fixed string escaping and formatting issues
    user_plan = user['plan']
    monthly_uploads = user['monthly_uploads']
    user_email = user.get('email') or ''
    user_name = user.get('name') or ''
    
    return f"""<!DOCTYPE html>
<html>
<head>
    <title>BJJ AI Analyzer Pro</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }}
        .glass {{ background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); }}
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}
        .tab-button.active {{ background: rgba(255, 255, 255, 0.2); }}
    </style>
</head>
<body class="min-h-screen">
    <div class="text-center py-8">
        <h1 class="text-5xl font-bold text-white mb-4">BJJ AI Analyzer Pro</h1>
        <p class="text-xl text-gray-200">Complete BJJ Analytics Platform</p>
        
        <div class="mt-6 mb-4" id="account-section">
            <div class="bg-yellow-600 bg-opacity-20 rounded-lg p-4 max-w-md mx-auto border border-yellow-500">
                <h3 class="text-lg font-bold text-white mb-2">Create Your Account</h3>
                <p class="text-yellow-100 text-sm mb-4">Save your progress and let AI learn your fighting style!</p>
                <div class="space-y-3">
                    <input type="email" id="userEmail" placeholder="Enter your email" 
                           class="w-full p-3 rounded-lg bg-white bg-opacity-20 text-white placeholder-gray-300">
                    <input type="text" id="userName" placeholder="Your name" 
                           class="w-full p-3 rounded-lg bg-white bg-opacity-20 text-white placeholder-gray-300">
                    <button onclick="createAccount()" class="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg font-bold w-full">
                        CREATE ACCOUNT
                    </button>
                </div>
            </div>
        </div>
        
        <div class="mt-4">
            <span class="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-lg text-lg font-bold" id="user-info">
                {user_plan.upper()} PLAN • {user['videos_count']} Videos Analyzed
            </span>
        </div>
        
        <div class="mt-4 space-x-4">
            <button onclick="showPricing()" class="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg font-bold text-lg">
                UPGRADE NOW
            </button>
            <span class="font-bold text-yellow-300" id="upload-counter">
                Monthly Uploads: {monthly_uploads}/{1 if user_plan == 'free' else 4 if user_plan == 'pro' else 'unlimited'}
            </span>
        </div>
    </div>

    <div id="pricing-modal" class="fixed inset-0 bg-black bg-opacity-75 hidden z-50 flex items-center justify-center">
        <div class="glass rounded-2xl p-8 max-w-6xl mx-4">
            <div class="flex justify-between items-center mb-8">
                <h2 class="text-3xl font-bold text-white">Choose Your BJJ Journey</h2>
                <button onclick="hidePricing()" class="text-white text-3xl hover:text-red-400">&times;</button>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div class="bg-gray-800 bg-opacity-50 rounded-xl p-6 text-center">
                    <h3 class="text-2xl font-bold text-white mb-4">Free</h3>
                    <div class="text-4xl font-bold text-white mb-6">$0/month</div>
                    <ul class="text-gray-300 space-y-3 mb-8 text-left">
                        <li>1 upload per month</li>
                        <li>Basic analytics</li>
                        <li>No timestamps</li>
                        <li>No breakdowns</li>
                    </ul>
                    <button class="bg-gray-600 text-white py-3 px-6 rounded-lg w-full font-bold">Current Plan</button>
                </div>
                
                <div class="bg-blue-600 bg-opacity-30 rounded-xl p-6 text-center border-2 border-blue-400">
                    <div class="bg-blue-500 text-white px-4 py-2 rounded-full text-sm mb-4">MOST POPULAR</div>
                    <h3 class="text-2xl font-bold text-white mb-4">Pro</h3>
                    <div class="text-4xl font-bold text-white mb-6">$29/month</div>
                    <ul class="text-white space-y-3 mb-8 text-left">
                        <li>4 uploads per month</li>
                        <li>Detailed breakdowns</li>
                        <li>Video timestamps</li>
                        <li>Advanced analytics</li>
                    </ul>
                    <button onclick="selectPlan('pro')" class="bg-blue-600 hover:bg-blue-700 text-white py-3 px-8 rounded-lg w-full font-bold">
                        UPGRADE TO PRO
                    </button>
                </div>
                
                <div class="bg-black bg-opacity-50 rounded-xl p-6 text-center border-2 border-yellow-400">
                    <div class="bg-yellow-500 text-black px-4 py-2 rounded-full text-sm mb-4 font-bold">BLACK BELT</div>
                    <h3 class="text-2xl font-bold text-white mb-4">Black Belt</h3>
                    <div class="text-4xl font-bold text-white mb-6">$59/month</div>
                    <ul class="text-yellow-100 space-y-3 mb-8 text-left">
                        <li>UNLIMITED uploads</li>
                        <li>Advanced breakdowns</li>
                        <li>Competition analytics</li>
                        <li>AI coaching</li>
                    </ul>
                    <button onclick="selectPlan('blackbelt')" class="bg-yellow-500 hover:bg-yellow-600 text-black py-3 px-8 rounded-lg w-full font-bold">
                        GO BLACK BELT
                    </button>
                </div>
            </div>
        </div>
    </div>

    <div class="container mx-auto px-4 max-w-6xl mb-8">
        <div class="glass rounded-xl p-2">
            <div class="flex flex-wrap justify-center space-x-2">
                <button onclick="showTab('upload')" class="tab-button active px-6 py-3 rounded-lg text-white font-semibold text-lg">Upload</button>
                <button onclick="showTab('submissions')" class="tab-button px-6 py-3 rounded-lg text-white font-semibold text-lg">Submissions</button>
                <button onclick="showTab('sweeps')" class="tab-button px-6 py-3 rounded-lg text-white font-semibold text-lg">Sweeps</button>
                <button onclick="showTab('takedowns')" class="tab-button px-6 py-3 rounded-lg text-white font-semibold text-lg">Takedowns</button>
                <button onclick="showTab('analytics')" class="tab-button px-6 py-3 rounded-lg text-white font-semibold text-lg">Analytics</button>
            </div>
        </div>
    </div>

    <div class="container mx-auto px-4 max-w-6xl">
        <div id="upload-tab" class="tab-content active">
            <div class="glass rounded-xl p-8">
                <h2 class="text-3xl font-bold text-white mb-8 text-center">Upload Your BJJ Video</h2>
                <div class="bg-gradient-to-r from-green-600 to-blue-600 rounded-xl p-8 text-center">
                    <h3 class="text-2xl font-bold text-white mb-4">Ready to Analyze Your Game?</h3>
                    <p class="text-white mb-6">Upload your training footage and get instant AI-powered technique analysis</p>
                    <input type="file" id="videoFile" accept="video/*" class="mb-6 text-white bg-white bg-opacity-20 p-4 rounded-lg">
                    <br>
                    <button onclick="analyzeVideo()" class="bg-white text-blue-600 font-bold py-4 px-8 rounded-lg text-xl hover:bg-gray-100" id="analyze-btn">
                        ANALYZE MY TECHNIQUES
                    </button>
                    <div class="mt-6 text-white">
                        <div id="upload-info">
                            <p>Monthly uploads remaining: <strong>{max(0, (1 if user_plan == 'free' else 4 if user_plan == 'pro' else 999) - monthly_uploads)}</strong></p>
                        </div>
                    </div>
                </div>
            </div>

            <div id="progress-section" class="glass rounded-xl p-8 mt-8 hidden">
                <h3 class="text-2xl font-bold text-white mb-6 text-center">AI Analyzing Your Techniques...</h3>
                <div class="w-full bg-gray-700 rounded-full h-6 mb-6">
                    <div id="progress-bar" class="bg-gradient-to-r from-green-500 to-blue-500 h-6 rounded-full transition-all duration-500" style="width: 0%"></div>
                </div>
                <p class="text-gray-300 text-center text-lg">Processing your BJJ footage with advanced AI...</p>
            </div>

            <div id="results-section" class="glass rounded-xl p-8 mt-8 hidden">
                <h3 class="text-3xl font-bold text-white mb-8 text-center">Your BJJ Analysis</h3>
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
                    <h4 class="text-2xl font-bold text-white mb-4">AI Insights</h4>
                    <div id="insights-list"></div>
                </div>
            </div>
        </div>

        <div id="submissions-tab" class="tab-content">
            <div class="glass rounded-xl p-8">
                <h2 class="text-3xl font-bold text-white mb-8 text-center">Submission Analysis</h2>
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
                    <div class="bg-gradient-to-br from-red-500 to-red-700 rounded-xl p-6">
                        <h3 class="text-xl font-bold text-white mb-4">Submission Stats</h3>
                        <div class="space-y-4">
                            <div class="flex justify-between">
                                <span class="text-red-100">Success Rate</span>
                                <span class="text-white font-bold" id="sub-success-rate">-</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-red-100">Avg Setup Time</span>
                                <span class="text-white font-bold" id="sub-avg-time">-</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-red-100">Total Attempts</span>
                                <span class="text-white font-bold" id="sub-total-attempts">-</span>
                            </div>
                        </div>
                    </div>
                    <div class="bg-white bg-opacity-10 rounded-xl p-6">
                        <h3 class="text-xl font-bold text-white mb-4">Top Submissions</h3>
                        <div id="top-submissions" class="space-y-3">
                            <p class="text-gray-300 text-center">Upload videos to see your top submissions!</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div id="sweeps-tab" class="tab-content">
            <div class="glass rounded-xl p-8">
                <h2 class="text-3xl font-bold text-white mb-8 text-center">Sweep Analysis</h2>
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
                    <div class="bg-gradient-to-br from-blue-500 to-blue-700 rounded-xl p-6">
                        <h3 class="text-xl font-bold text-white mb-4">Sweep Stats</h3>
                        <div class="space-y-4">
                            <div class="flex justify-between">
                                <span class="text-blue-100">Success Rate</span>
                                <span class="text-white font-bold" id="sweep-success-rate">-</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-blue-100">Total Attempts</span>
                                <span class="text-white font-bold" id="sweep-total-attempts">-</span>
                            </div>
                        </div>
                    </div>
                    <div class="bg-white bg-opacity-10 rounded-xl p-6">
                        <h3 class="text-xl font-bold text-white mb-4">Top Sweeps</h3>
                        <div id="top-sweeps" class="space-y-3">
                            <p class="text-gray-300 text-center">Upload videos to see your top sweeps!</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div id="takedowns-tab" class="tab-content">
            <div class="glass rounded-xl p-8">
                <h2 class="text-3xl font-bold text-white mb-8 text-center">Takedown Analysis</h2>
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
                    <div class="bg-gradient-to-br from-orange-500 to-orange-700 rounded-xl p-6">
                        <h3 class="text-xl font-bold text-white mb-4">Takedown Stats</h3>
                        <div class="space-y-4">
                            <div class="flex justify-between">
                                <span class="text-orange-100">Success Rate</span>
                                <span class="text-white font-bold" id="takedown-success-rate">-</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-orange-100">Total Attempts</span>
                                <span class="text-white font-bold" id="takedown-total-attempts">-</span>
                            </div>
                        </div>
                    </div>
                    <div class="bg-white bg-opacity-10 rounded-xl p-6">
                        <h3 class="text-xl font-bold text-white mb-4">Top Takedowns</h3>
                        <div id="top-takedowns" class="space-y-3">
                            <p class="text-gray-300 text-center">Upload videos to see your top takedowns!</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div id="analytics-tab" class="tab-content">
            <div class="glass rounded-xl p-8">
                <h2 class="text-3xl font-bold text-white mb-8 text-center">Your BJJ Analytics</h2>
                <div class="bg-gradient-to-r from-purple-600 to-blue-600 rounded-xl p-6 mb-8">
                    <h3 class="text-2xl font-bold text-white mb-4">Overall Performance</h3>
                    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                        <div class="bg-white bg-opacity-20 rounded-lg p-4 text-center">
                            <div class="text-2xl font-bold text-white" id="total-videos">{user['videos_count']}</div>
                            <div class="text-purple-100">Videos</div>
                        </div>
                        <div class="bg-white bg-opacity-20 rounded-lg p-4 text-center">
                            <div class="text-2xl font-bold text-white" id="total-techniques">0</div>
                            <div class="text-purple-100">Techniques</div>
                        </div>
                        <div class="bg-white bg-opacity-20 rounded-lg p-4 text-center">
                            <div class="text-2xl font-bold text-white" id="overall-rate">0%</div>
                            <div class="text-purple-100">Success Rate</div>
                        </div>
                        <div class="bg-white bg-opacity-20 rounded-lg p-4 text-center">
                            <div class="text-2xl font-bold text-white">+12%</div>
                            <div class="text-purple-100">Improvement</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let userPlan = '{user_plan}';
        let monthlyUploads = {monthly_uploads};
        let userEmail = '{user_email}';
        let userName = '{user_name}';

        function createAccount() {{
            const email = document.getElementById('userEmail').value.trim();
            const name = document.getElementById('userName').value.trim();
            
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
            .then(response =>
