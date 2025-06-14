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
access_codes = {
    'BJJ2024FREE': {'plan': 'elite', 'uses': 100},
    'GUARD2024': {'plan': 'elite', 'uses': 100},
    'SWEEP2024': {'plan': 'elite', 'uses': 100},
    'SUBMIT2024': {'plan': 'elite', 'uses': 100},
    'ESCAPE2024': {'plan': 'elite', 'uses': 100}
}

# Demo stats
demo_stats = {
    'submission_rates': {'armbar': 87, 'triangle': 72, 'rnc': 95, 'kimura': 65, 'heel_hook': 81},
    'sweep_rates': {'tripod': 92, 'scissor': 68, 'butterfly': 81, 'flower': 55, 'dlr': 73},
    'pass_rates': {'knee_cut': 82, 'toreando': 75, 'leg_drag': 88, 'stack': 60},
    'takedown_rates': {'double_leg': 70, 'single_leg': 55, 'hip_toss': 45, 'foot_sweep': 38}
}

def get_user_id():
    if 'user_id' not in session:
        session['user_id'] = f"user_{random.randint(1000, 9999)}"
        users[session['user_id']] = {
            'plan': 'demo',
            'videos_count': 0,
            'created_at': datetime.now().isoformat()
        }
        user_videos[session['user_id']] = []
    return session['user_id']

def generate_analysis(plan):
    techniques = []
    
    # Generate techniques based on plan
    technique_list = [
        {'name': 'armbar_from_guard', 'cat': 'submission'},
        {'name': 'triangle_choke', 'cat': 'submission'},
        {'name': 'rear_naked_choke', 'cat': 'submission'},
        {'name': 'kimura', 'cat': 'submission'},
        {'name': 'tripod_sweep', 'cat': 'sweep'},
        {'name': 'scissor_sweep', 'cat': 'sweep'},
        {'name': 'butterfly_sweep', 'cat': 'sweep'},
        {'name': 'knee_cut_pass', 'cat': 'guard_pass'},
        {'name': 'toreando_pass', 'cat': 'guard_pass'},
        {'name': 'double_leg_takedown', 'cat': 'takedown'},
        {'name': 'single_leg_takedown', 'cat': 'takedown'},
        {'name': 'guard_retention', 'cat': 'position'}
    ]
    
    # Demo users get limited analysis
    if plan == 'demo':
        num_techniques = random.randint(3, 5)  # Fewer techniques
        selected = random.sample(technique_list, num_techniques)
    else:
        num_techniques = random.randint(8, 12)
        selected = random.sample(technique_list, num_techniques)
    
    for i, tech in enumerate(selected):
        start_time = random.randint(10, 240)
        techniques.append({
            'technique': tech['name'],
            'category': tech['cat'],
            'confidence': round(random.uniform(0.7, 0.98), 2),
            'start_time': start_time,
            'end_time': start_time + random.randint(8, 20),
            'quality': random.choice(['excellent', 'good', 'fair']),
            'position': random.choice(['guard', 'mount', 'side_control', 'standing']),
            'has_timestamp': (plan == 'elite')
        })
    
    # Different insights based on plan
    if plan == 'demo':
        insights = [
            "🎯 Basic technique detection working! Upgrade for detailed analysis.",
            "📊 Limited demo analysis - subscribe for full insights."
        ]
    else:
        insights = [
            "🎯 Great technique diversity! You're showing skills across multiple categories.",
            "🔥 High execution quality detected in your submissions.",
            "🌊 Strong guard game - you're comfortable working from bottom.",
            "📈 Consistent performance across different positions."
        ]
    
    return {
        'total_techniques_detected': len(techniques),
        'detected_techniques': techniques,
        'video_duration': random.randint(180, 300),
        'techniques_per_minute': round(len(techniques) / 4, 1),
        'average_confidence': round(sum(t['confidence'] for t in techniques) / len(techniques), 2),
        'insights': random.sample(insights, min(len(insights), 3)),
        'analysis_timestamp': datetime.now().isoformat(),
        'user_plan': plan
    }

@app.route('/')
def home():
    user_id = get_user_id()
    user_plan = users[user_id]['plan']
    video_count = len(user_videos.get(user_id, []))
    
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BJJ AI Analyzer Pro</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .glass { background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        .tab-button.active { background: rgba(255, 255, 255, 0.2); }
        .demo-badge { position: absolute; top: 5px; right: 5px; background: rgba(255, 193, 7, 0.9); color: black; padding: 2px 6px; border-radius: 3px; font-size: 10px; }
    </style>
</head>
<body class="min-h-screen">
    <div class="text-center py-8">
        <h1 class="text-5xl font-bold text-white mb-4">🥋 BJJ AI Analyzer Pro</h1>
        <p class="text-xl text-gray-200">Complete BJJ Analytics Platform</p>
        <div class="mt-4">'''
    
    if user_plan != 'demo':
        html += f'''<span class="bg-green-600 text-white px-4 py-2 rounded-lg">
            ✅ {user_plan.upper()} MEMBER • {video_count} Videos
        </span>'''
    else:
        demo_uploads_used = video_count
        html += f'''<div class="space-x-4">
            <span class="bg-orange-600 text-white px-3 py-2 rounded-lg text-sm">
                🆓 DEMO • {demo_uploads_used}/1 Free Upload Used
            </span>
            <button onclick="showAccessCode()" class="bg-yellow-600 hover:bg-yellow-700 text-white px-4 py-2 rounded-lg font-bold">
                🎁 Elite Access Code?
            </button>
            <button onclick="showPricing()" class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-bold">
                🚀 SUBSCRIBE NOW
            </button>
        </div>'''
    
    html += '''</div>
    </div>

    <!-- Access Code Modal -->
    <div id="access-code-modal" class="fixed inset-0 bg-black bg-opacity-50 hidden z-50 flex items-center justify-center">
        <div class="glass rounded-xl p-8 max-w-md mx-4">
            <h2 class="text-2xl font-bold text-white mb-4">🎁 Elite Access Code</h2>
            <p class="text-gray-300 mb-4">Got a code for free Elite access? Enter it here!</p>
            <input type="text" id="access-code-input" placeholder="Enter elite access code" 
                   class="w-full p-3 rounded-lg bg-white bg-opacity-20 text-white placeholder-gray-300 mb-4">
            <div class="space-x-4">
                <button onclick="redeemCode()" class="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg font-bold">
                    Redeem Elite
                </button>
                <button onclick="hideAccessCode()" class="bg-gray-600 hover:bg-gray-700 text-white px-6 py-2 rounded-lg">
                    Cancel
                </button>
            </div>
            <p class="text-gray-300 text-sm mt-4">Try: BJJ2024FREE, GUARD2024, SWEEP2024</p>
        </div>
    </div>

    <!-- Pricing Modal -->
    <div id="pricing-modal" class="fixed inset-0 bg-black bg-opacity-50 hidden z-50 flex items-center justify-center">
        <div class="glass rounded-xl p-8 max-w-4xl mx-4">
            <div class="flex justify-between items-center mb-6">
                <h2 class="text-2xl font-bold text-white">Choose Your Plan</h2>
                <button onclick="hidePricing()" class="text-white text-2xl">&times;</button>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="bg-white bg-opacity-10 rounded-lg p-6 text-center">
                    <h3 class="text-xl font-bold text-white mb-2">Demo</h3>
                    <div class="text-3xl font-bold text-white mb-4">$0</div>
                    <ul class="text-gray-300 space-y-2 mb-6 text-sm">
                        <li>• 1 free upload</li>
                        <li>• Limited analysis</li>
                        <li>• Demo data view</li>
                    </ul>
                    <button onclick="alert('You are already on Demo!')" class="bg-gray-600 text-white py-2 px-4 rounded-lg w-full">
                        Current Plan
                    </button>
                </div>
                <div class="bg-blue-600 bg-opacity-20 rounded-lg p-6 text-center border-2 border-blue-400">
                    <div class="bg-blue-500 text-white px-3 py-1 rounded-full text-xs mb-2">POPULAR</div>
                    <h3 class="text-xl font-bold text-white mb-2">BJJ Pro</h3>
                    <div class="text-3xl font-bold text-white mb-4">$20</div>
                    <ul class="text-white space-y-2 mb-6 text-sm">
                        <li>• Unlimited videos</li>
                        <li>• Full analytics</li>
                        <li>• Progress tracking</li>
                    </ul>
                    <button onclick="subscribePlan('pro')" class="bg-blue-600 hover:bg-blue-700 text-white py-2 px-6 rounded-lg w-full">
                        Subscribe
                    </button>
                </div>
                <div class="bg-purple-600 bg-opacity-20 rounded-lg p-6 text-center border-2 border-purple-400">
                    <div class="bg-purple-500 text-white px-3 py-1 rounded-full text-xs mb-2">ELITE</div>
                    <h3 class="text-xl font-bold text-white mb-2">Elite</h3>
                    <div class="text-3xl font-bold text-white mb-4">$50</div>
                    <ul class="text-white space-y-2 mb-6 text-sm">
                        <li>• Everything in Pro</li>
                        <li>• Video timestamps</li>
                        <li>• Competition tools</li>
                    </ul>
                    <button onclick="subscribePlan('elite')" class="bg-purple-600 hover:bg-purple-700 text-white py-2 px-6 rounded-lg w-full">
                        Subscribe
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Navigation -->
    <div class="container mx-auto px-4 max-w-6xl mb-8">
        <div class="glass rounded-xl p-2">
            <div class="flex flex-wrap justify-center space-x-2">
                <button onclick="showTab('upload')" class="tab-button active px-4 py-2 rounded-lg text-white font-semibold">
                    📹 Upload
                </button>
                <button onclick="showTab('submissions')" class="tab-button px-4 py-2 rounded-lg text-white font-semibold relative">
                    🎯 Submissions'''
    
    if user_plan == 'demo':
        html += '<span class="demo-badge">DEMO</span>'
    
    html += '''</button>
                <button onclick="showTab('sweeps')" class="tab-button px-4 py-2 rounded-lg text-white font-semibold relative">
                    🌊 Sweeps'''
    
    if user_plan == 'demo':
        html += '<span class="demo-badge">DEMO</span>'
    
    html += '''</button>
                <button onclick="showTab('passes')" class="tab-button px-4 py-2 rounded-lg text-white font-semibold relative">
                    🛡️ Passes'''
    
    if user_plan == 'demo':
        html += '<span class="demo-badge">DEMO</span>'
    
    html += '''</button>
                <button onclick="showTab('takedowns')" class="tab-button px-4 py-2 rounded-lg text-white font-semibold relative">
                    🤼 Takedowns'''
    
    if user_plan == 'demo':
        html += '<span class="demo-badge">DEMO</span>'
    
    html += '''</button>
                <button onclick="showTab('analytics')" class="tab-button px-4 py-2 rounded-lg text-white font-semibold relative">
                    📊 Analytics'''
    
    if user_plan == 'demo':
        html += '<span class="demo-badge">DEMO</span>'
    
    html += '''</button>
            </div>
        </div>
    </div>

    <div class="container mx-auto px-4 max-w-6xl">
        <!-- Upload Tab -->
        <div id="upload-tab" class="tab-content active">
            <div class="glass rounded-xl p-8 mb-8">
                <h2 class="text-2xl font-bold text-white mb-6 text-center">Upload Your BJJ Video</h2>'''
    
    demo_uploads_used = video_count if user_plan == 'demo' else 0
    
    if user_plan == 'demo' and demo_uploads_used >= 1:
        html += '''<div class="bg-orange-900 bg-opacity-50 rounded-lg p-6 text-center mb-6">
                    <h3 class="text-xl font-bold text-white mb-2">🆓 Free Upload Used</h3>
                    <p class="text-gray-300 mb-4">You've used your 1 free demo upload. Get elite access or subscribe for unlimited uploads!</p>
                    <div class="space-x-4">
                        <button onclick="showAccessCode()" class="bg-yellow-600 hover:bg-yellow-700 text-white font-bold py-2 px-4 rounded-lg">
                            🎁 Use Elite Code
                        </button>
                        <button onclick="showPricing()" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg">
                            Subscribe
                        </button>
                    </div>
                </div>'''
    elif user_plan == 'demo':
        html += f'''<div class="bg-green-900 bg-opacity-50 rounded-lg p-6 text-center mb-6">
                    <h3 class="text-xl font-bold text-white mb-2">🆓 Free Demo Upload</h3>
                    <p class="text-gray-300 mb-4">Try our AI analysis with 1 free upload! Limited breakdown included.</p>
                    <p class="text-yellow-300 text-sm">After this, use an elite access code or subscribe for unlimited uploads.</p>
                </div>
                <div class="text-center">
                    <input type="file" id="videoFile" accept="video/*" class="mb-4 text-white">
                    <br>
                    <p class="text-orange-300 text-sm mb-4">🆓 Demo Plan - Basic analysis (upgrade for full features)</p>
                    <button onclick="analyzeVideo()" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-lg">
                        🤖 Try AI Analysis
                    </button>
                </div>'''
    else:
        html += f'''<div class="text-center">
                    <input type="file" id="videoFile" accept="video/*" class="mb-4 text-white">
                    <br>
                    <p class="text-green-300 text-sm mb-4">✅ {user_plan.title()} Plan - Full analysis</p>
                    <button onclick="analyzeVideo()" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-lg">
                        🤖 Analyze Techniques
                    </button>'''
        
        if user_plan == 'elite':
            html += '<p class="text-purple-300 text-xs mt-2">🎬 Elite: Video timestamps included!</p>'
        
        html += '</div>'
    
    html += '''</div>

            <!-- Progress Section -->
            <div id="progress-section" class="glass rounded-xl p-6 mb-8 hidden">
                <h3 class="text-xl font-bold text-white mb-4">🔍 Analyzing Your Video...</h3>
                <div class="w-full bg-gray-700 rounded-full h-4 mb-4">
                    <div id="progress-bar" class="bg-blue-600 h-4 rounded-full transition-all duration-500" style="width: 0%"></div>
                </div>
                <p class="text-gray-300 text-center">🧠 AI is detecting BJJ techniques...</p>
            </div>

            <!-- Results Section -->
            <div id="results-section" class="glass rounded-xl p-8 mb-8 hidden">
                <h3 class="text-2xl font-bold text-white mb-6">📊 Analysis Results</h3>
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                    <div class="bg-white bg-opacity-20 rounded-lg p-4 text-center">
                        <div class="text-2xl font-bold text-white" id="total-count">0</div>
                        <div class="text-gray-300 text-sm">Techniques</div>
                    </div>
                    <div class="bg-white bg-opacity-20 rounded-lg p-4 text-center">
                        <div class="text-2xl font-bold text-white" id="avg-confidence">0%</div>
                        <div class="text-gray-300 text-sm">Confidence</div>
                    </div>
                    <div class="bg-white bg-opacity-20 rounded-lg p-4 text-center">
                        <div class="text-2xl font-bold text-white" id="video-duration">0s</div>
                        <div class="text-gray-300 text-sm">Duration</div>
                    </div>
                    <div class="bg-white bg-opacity-20 rounded-lg p-4 text-center">
                        <div class="text-2xl font-bold text-white" id="submission-count">0</div>
                        <div class="text-gray-300 text-sm">Submissions</div>
                    </div>
                </div>
                <div id="techniques-list" class="space-y-4 mb-6"></div>
                <div id="insights-section" class="bg-white bg-opacity-10 rounded-lg p-6 mb-6">
                    <h4 class="text-lg font-bold text-white mb-4">🧠 AI Insights</h4>
                    <div id="insights-list"></div>
                </div>
                <div class="text-center">
                    <button onclick="resetApp()" class="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-6 rounded-lg">
                        📹 Analyze Another Video
                    </button>
                </div>
            </div>
        </div>

        <!-- Submissions Tab -->
        <div id="submissions-tab" class="tab-content">
            <div class="glass rounded-xl p-8">
                <h2 class="text-2xl font-bold text-white mb-6">🎯 Submission Analytics</h2>
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    <div class="bg-white bg-opacity-10 rounded-lg p-6">
                        <h3 class="text-xl font-bold text-white mb-4">Success Rates</h3>
                        <canvas id="submission-chart" width="400" height="300"></canvas>
                    </div>
                    <div class="bg-white bg-opacity-10 rounded-lg p-6">
                        <h3 class="text-xl font-bold text-white mb-4">Vulnerability Analysis</h3>
                        <div class="space-y-3">
                            <div class="flex justify-between">
                                <span class="text-gray-300">Heel Hook</span>
                                <span class="text-red-400 font-bold">67%</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-gray-300">Triangle</span>
                                <span class="text-yellow-400 font-bold">45%</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-gray-300">RNC</span>
                                <span class="text-green-400 font-bold">32%</span>
                            </div>
                        </div>
                        <div class="mt-6">
                            <h4 class="font-bold text-white mb-2">🎯 Training Focus</h4>
                            <div class="bg-red-900 bg-opacity-50 rounded p-3">
                                <p class="text-red-300 text-sm">Priority: Heel hook defense</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Sweeps Tab -->
        <div id="sweeps-tab" class="tab-content">
            <div class="glass rounded-xl p-8">
                <h2 class="text-2xl font-bold text-white mb-6">🌊 Sweep Analytics</h2>
                <div class="bg-white bg-opacity-10 rounded-lg p-6">
                    <h3 class="text-xl font-bold text-white mb-4">Your Best Sweeps</h3>
                    <canvas id="sweep-chart" width="400" height="300"></canvas>
                </div>
            </div>
        </div>

        <!-- Guard Passes Tab -->
        <div id="passes-tab" class="tab-content">
            <div class="glass rounded-xl p-8">
                <h2 class="text-2xl font-bold text-white mb-6">🛡️ Guard Pass Analytics</h2>
                <div class="bg-white bg-opacity-10 rounded-lg p-6">
                    <h3 class="text-xl font-bold text-white mb-4">Passing Success</h3>
                    <canvas id="pass-chart" width="400" height="300"></canvas>
                </div>
            </div>
        </div>

        <!-- Takedowns Tab -->
        <div id="takedowns-tab" class="tab-content">
            <div class="glass rounded-xl p-8">
                <h2 class="text-2xl font-bold text-white mb-6">🤼 Takedown Analytics</h2>
                <div class="bg-white bg-opacity-10 rounded-lg p-6">
                    <h3 class="text-xl font-bold text-white mb-4">Success Rates</h3>
                    <canvas id="takedown-chart" width="400" height="300"></canvas>
                </div>
            </div>
        </div>

        <!-- Analytics Tab -->
        <div id="analytics-tab" class="tab-content">
            <div class="glass rounded-xl p-8">
                <h2 class="text-2xl font-bold text-white mb-6">📊 Complete Analytics</h2>
                <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                    <div class="bg-gradient-to-br from-blue-600 to-blue-800 rounded-lg p-6 text-center">
                        <div class="text-3xl font-bold text-white">B+</div>
                        <div class="text-blue-200">Overall Grade</div>
                    </div>
                    <div class="bg-gradient-to-br from-green-600 to-green-800 rounded-lg p-6 text-center">
                        <div class="text-3xl font-bold text-white">78%</div>
                        <div class="text-green-200">Success Rate</div>
                    </div>
                    <div class="bg-gradient-to-br from-purple-600 to-purple-800 rounded-lg p-6 text-center">
                        <div class="text-3xl font-bold text-white">''' + str(video_count) + '''</div>
                        <div class="text-purple-200">Videos</div>
                    </div>
                    <div class="bg-gradient-to-br from-orange-600 to-orange-800 rounded-lg p-6 text-center">
                        <div class="text-3xl font-bold text-white">+15%</div>
                        <div class="text-orange-200">This Month</div>
                    </div>
                </div>
                <div class="bg-white bg-opacity-10 rounded-lg p-6">
                    <h3 class="text-xl font-bold text-white mb-4">🎭 BJJ Style Profile</h3>
                    <div class="space-y-4">
                        <div>
                            <div class="flex justify-between mb-1">
                                <span class="text-gray-300">Guard Player</span>
                                <span class="text-white">85%</span>
                            </div>
                            <div class="w-full bg-gray-700 rounded-full h-2">
                                <div class="bg-blue-500 h-2 rounded-full" style="width: 85%"></div>
                            </div>
                        </div>
                        <div>
                            <div class="flex justify-between mb-1">
                                <span class="text-gray-300">Submission Hunter</span>
                                <span class="text-white">91%</span>
                            </div>
                            <div class="w-full bg-gray-700 rounded-full h-2">
                                <div class="bg-red-500 h-2 rounded-full" style="width: 91%"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="text-center py-8 mt-8">
        <p class="text-gray-400 text-sm">BJJ AI Analyzer Pro | Complete Analytics Platform</p>
    </div>

    <script>
        const userPlan = "''' + user_plan + '''";

        function showTab(tabName) {
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            document.querySelectorAll('.tab-button').forEach(btn => {
                btn.classList.remove('active');
            });
            document.getElementById(tabName + '-tab').classList.add('active');
            event.target.classList.add('active');
            
            if (tabName === 'submissions') setTimeout(initSubmissionChart, 100);
            else if (tabName === 'sweeps') setTimeout(initSweepChart, 100);
            else if (tabName === 'passes') setTimeout(initPassChart, 100);
            else if (tabName === 'takedowns') setTimeout(initTakedownChart, 100);
        }

        function showAccessCode() {
            document.getElementById('access-code-modal').classList.remove('hidden');
        }

        function hideAccessCode() {
            document.getElementById('access-code-modal').classList.add('hidden');
        }

        function showPricing() {
            document.getElementById('pricing-modal').classList.remove('hidden');
        }

        function hidePricing() {
            document.getElementById('pricing-modal').classList.add('hidden');
        }

        async function redeemCode() {
            const code = document.getElementById('access-code-input').value.trim();
            if (!code) return alert('Enter a code');

            try {
                const response = await fetch('/api/redeem-code', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({code: code})
                });
                const result = await response.json();
                
                if (result.success) {
                    alert('🎉 Elite access activated! Refreshing...');
                    location.reload();
                } else {
                    alert('❌ ' + result.message);
                }
            } catch (error) {
                alert('Error: ' + error.message);
            }
        }

        function subscribePlan(plan) {
            alert(`🚀 Subscribing to ${plan.toUpperCase()}!\\n\\nPayment integration would go here.\\n\\nFor demo: use BJJ2024FREE for elite access`);
        }

        async function analyzeVideo() {
            const fileInput = document.getElementById('videoFile');
            if (!fileInput.files[0]) return alert('Select a video first!');

            document.getElementById('progress-section').classList.remove('hidden');

            let progress = 0;
            const progressBar = document.getElementById('progress-bar');
            
            const interval = setInterval(() => {
                progress += Math.random() * 15;
                if (progress > 100) progress = 100;
                progressBar.style.width = progress + '%';
                
                if (progress >= 100) {
                    clearInterval(interval);
                    performAnalysis();
                }
            }, 300);
        }

        async function performAnalysis() {
            try {
                const formData = new FormData();
                formData.append('video', document.getElementById('videoFile').files[0]);

                const response = await fetch('/api/analyze', {
                    method: 'POST',
                    body: formData
                });

                const results = await response.json();
                if (results.error) {
                    alert('❌ ' + results.error);
                    resetApp();
                    return;
                }
                
                displayResults(results);
            } catch (error) {
                alert('Analysis failed: ' + error.message);
                resetApp();
            }
        }

        function displayResults(results) {
            document.getElementById('progress-section').classList.add('hidden');
            document.getElementById('results-section').classList.remove('hidden');

            document.getElementById('total-count').textContent = results.total_techniques_detected;
            document.getElementById('avg-confidence').textContent = Math.round(results.average_confidence * 100) + '%';
            document.getElementById('video-duration').textContent = results.video_duration + 's';
            
            const submissionCount = results.detected_techniques.filter(t => t.category === 'submission').length;
            document.getElementById('submission-count').textContent = submissionCount;

            displayTechniques(results.detected_techniques);
            displayInsights(results.insights);
        }

        function displayTechniques(techniques) {
            const techniquesList = document.getElementById('techniques-list');
            techniquesList.innerHTML = '';

            techniques.forEach(technique => {
                const categoryColors = {
                    'submission': 'border-l-red-500 bg-red-900',
                    'sweep': 'border-l-blue-500 bg-blue-900',
                    'guard_pass': 'border-l-green-500 bg-green-900',
                    'takedown': 'border-l-yellow-500 bg-yellow-900',
                    'position': 'border-l-purple-500 bg-purple-900'
                };

                const qualityColors = {
                    'excellent': 'text-green-400',
                    'good': 'text-yellow-400',
                    'fair': 'text-orange-400'
                };

                const categoryColor = categoryColors[technique.category] || 'border-l-gray-500 bg-gray-900';
                const qualityColor = qualityColors[technique.quality] || 'text-gray-400';

                const techniqueDiv = document.createElement('div');
                techniqueDiv.className = `${categoryColor} bg-opacity-30 border-l-4 rounded-lg p-4`;
                
                let timestampHTML = '';
                if (technique.has_timestamp) {
                    timestampHTML = `
                        <button onclick="jumpToTime(${technique.start_time})" 
                                class="bg-blue-600 hover:bg-blue-700 text-white px-2 py-1 rounded text-xs ml-2">
                            🎬 ${formatTime(technique.start_time)}
                        </button>
                    `;
                }

                techniqueDiv.innerHTML = `
                    <div class="flex justify-between items-center">
                        <div class="flex-1">
                            <div class="flex items-center space-x-2 mb-1">
                                <h4 class="text-lg font-bold text-white">${formatTechniqueName(technique.technique)}</h4>
                                <span class="px-2 py-1 bg-white bg-opacity-20 rounded text-xs text-gray-300">
                                    ${technique.category.replace('_', ' ').toUpperCase()}
                                </span>
                                ${timestampHTML}
                            </div>
                            <p class="text-gray-300 text-sm">
                                Time: ${formatTime(technique.start_time)} - ${formatTime(technique.end_time)} | 
                                Position: ${technique.position}
                            </p>
                        </div>
                        <div class="text-right">
                            <div class="text-white font-bold text-lg">${Math.round(technique.confidence * 100)}%</div>
                            <div class="text-sm ${qualityColor} font-semibold">${technique.quality.toUpperCase()}</div>
                        </div>
                    </div>
                `;
                
                techniquesList.appendChild(techniqueDiv);
            });
        }

        function jumpToTime(seconds) {
            alert(`🎬 Elite Feature: Jump to ${formatTime(seconds)}\\n\\nIn full app, this would seek video to exact moment!`);
        }

        function displayInsights(insights) {
            const insightsList = document.getElementById('insights-list');
            insightsList.innerHTML = '';

            insights.forEach(insight => {
                const insightDiv = document.createElement('div');
                insightDiv.className = 'bg-white bg-opacity-10 rounded p-3 mb-2';
                insightDiv.innerHTML = `<p class="text-gray-300">${insight}</p>`;
                insightsList.appendChild(insightDiv);
            });
        }

        function initSubmissionChart() {
            const ctx = document.getElementById('submission-chart');
            if (!ctx || ctx.chart) return;

            ctx.chart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Armbar', 'Triangle', 'RNC', 'Kimura', 'Heel Hook'],
                    datasets: [{
                        data: [87, 72, 95, 65, 81],
                        backgroundColor: ['#ef4444', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6']
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { labels: { color: 'white' } }
                    }
                }
            });
        }

        function initSweepChart() {
            const ctx = document.getElementById('sweep-chart');
            if (!ctx || ctx.chart) return;

            ctx.chart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Tripod', 'Scissor', 'Butterfly', 'Flower', 'DLR'],
                    datasets: [{
                        label: 'Success Rate %',
                        data: [92, 68, 81, 55, 73],
                        backgroundColor: '#3b82f6'
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { ticks: { color: 'white' } },
                        x: { ticks: { color: 'white' } }
                    },
                    plugins: {
                        legend: { labels: { color: 'white' } }
                    }
                }
            });
        }

        function initPassChart() {
            const ctx = document.getElementById('pass-chart');
            if (!ctx || ctx.chart) return;

            ctx.chart = new Chart(ctx, {
                type: 'polarArea',
                data: {
                    labels: ['Knee Cut', 'Toreando', 'Leg Drag', 'Stack'],
                    datasets: [{
                        data: [82, 75, 88, 60],
                        backgroundColor: ['#ef4444', '#3b82f6', '#10b981', '#f59e0b']
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { labels: { color: 'white' } }
                    },
                    scales: {
                        r: { ticks: { color: 'white' } }
                    }
                }
            });
        }

        function initTakedownChart() {
            const ctx = document.getElementById('takedown-chart');
            if (!ctx || ctx.chart) return;

            ctx.chart = new Chart(ctx, {
                type: 'radar',
                data: {
                    labels: ['Double Leg', 'Single Leg', 'Hip Toss', 'Foot Sweep'],
                    datasets: [{
                        label: 'Success Rate',
                        data: [70, 55, 45, 38],
                        borderColor: '#3b82f6',
                        backgroundColor: 'rgba(59, 130, 246, 0.2)'
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { labels: { color: 'white' } }
                    },
                    scales: {
                        r: { 
                            ticks: { color: 'white' },
                            pointLabels: { color: 'white' }
                        }
                    }
                }
            });
        }

        function formatTechniqueName(name) {
            return name.replace(/_/g, ' ')
                      .split(' ')
                      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                      .join(' ');
        }

        function formatTime(seconds) {
            const mins = Math.floor(seconds / 60);
            const secs = Math.floor(seconds % 60);
            return `${mins}:${secs.toString().padStart(2, '0')}`;
        }

        function resetApp() {
            document.getElementById('progress-section').classList.add('hidden');
            document.getElementById('results-section').classList.add('hidden');
            document.getElementById('videoFile').value = '';
        }

        // Initialize first chart
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(initSubmissionChart, 500);
        });
    </script>
</body>
</html>'''
    
    return html

@app.route('/api/redeem-code', methods=['POST'])
def redeem_code():
    user_id = get_user_id()
    data = request.get_json()
    code = data.get('code', '').upper()
    
    if code in access_codes and access_codes[code]['uses'] > 0:
        access_codes[code]['uses'] -= 1
        users[user_id]['plan'] = access_codes[code]['plan']
        return jsonify({'success': True, 'message': f'Elite access activated! You now have unlimited uploads with full analysis.'})
    else:
        return jsonify({'success': False, 'message': 'Invalid or expired access code'})

@app.route('/api/analyze', methods=['POST'])
def analyze():
    user_id = get_user_id()
    user_plan = users[user_id]['plan']
    
    # Demo users get 1 free upload
    if user_plan == 'demo':
        demo_uploads_used = len(user_videos.get(user_id, []))
        if demo_uploads_used >= 1:
            return jsonify({'error': 'Demo limit reached! Use elite access code or subscribe for unlimited uploads.'}), 403
    
    # Check monthly limit for free users (if we had a free plan)
    if user_plan == 'free':
        current_month = datetime.now().strftime('%Y-%m')
        monthly_videos = [v for v in user_videos.get(user_id, []) if v.get('timestamp', '').startswith(current_month)]
        if len(monthly_videos) >= 1:
            return jsonify({'error': 'Free plan limit: 1 video per month. Upgrade to Pro!'}), 403
    
    # Simulate processing
    time.sleep(3)
    
    # Generate analysis
    analysis_result = generate_analysis(user_plan)
    
    # Store the analysis
    analysis_result['id'] = f"analysis_{len(user_videos.get(user_id, []))}"
    analysis_result['timestamp'] = datetime.now().isoformat()
    
    if user_id not in user_videos:
        user_videos[user_id] = []
    user_videos[user_id].append(analysis_result)
    
    users[user_id]['videos_count'] += 1
    
    return jsonify(analysis_result)

@app.route('/api/stats')
def get_stats():
    user_id = get_user_id()
    user_plan = users[user_id]['plan']
    
    if user_plan == 'demo':
        return jsonify(demo_stats)
    
    videos = user_videos.get(user_id, [])
    if not videos:
        return jsonify({'message': 'Upload videos to see real stats'})
    
    return jsonify({
        'total_videos': len(videos),
        'plan': user_plan,
        'latest_analysis': videos[-1] if videos else None
    })

@app.route('/health')
def health():
    return jsonify({'status': 'running', 'message': 'BJJ AI Analyzer Pro is online!'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
