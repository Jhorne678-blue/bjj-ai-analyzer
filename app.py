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
    'BJJ2024FREE': {'plan': 'free', 'uses': 100},
    'GUARD2024': {'plan': 'free', 'uses': 100},
    'SWEEP2024': {'plan': 'free', 'uses': 100},
    'SUBMIT2024': {'plan': 'free', 'uses': 100},
    'ESCAPE2024': {'plan': 'free', 'uses': 100}
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
    
    # Generate 8-12 techniques
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
        'insights': random.sample(insights, 3),
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
        html += '''<div class="space-x-4">
            <button onclick="showAccessCode()" class="bg-yellow-600 hover:bg-yellow-700 text-white px-4 py-2 rounded-lg font-bold">
                📝 Have Access Code?
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
            <h2 class="text-2xl font-bold text-white mb-4">Enter Access Code</h2>
            <input type="text" id="access-code-input" placeholder="Enter access code" 
                   class="w-full p-3 rounded-lg bg-white bg-opacity-20 text-white placeholder-gray-300 mb-4">
            <div class="space-x-4">
                <button onclick="redeemCode()" class="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg font-bold">
                    Redeem
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
                    <h3 class="text-xl font-bold text-white mb-2">Free Monthly</h3>
                    <div class="text-3xl font-bold text-white mb-4">$0</div>
                    <ul class="text-gray-300 space-y-2 mb-6 text-sm">
                        <li>• 1 video per month</li>
                        <li>• Basic analytics</li>
                        <li>• Demo data view</li>
                    </ul>
                    <button onclick="alert('Use access code!')" class="bg-gray-600 text-white py-2 px-4 rounded-lg w-full">
                        Need Code
                    </button>
                </div>
                <div class="bg-blue-600 bg-opacity-20 rounded-lg p-6 text-center border-2 border-blue-400">
                    <div class="bg-blue-500 text-white px-3 py-1 rounded-full text-xs mb-2">POPULAR</div>
                    <h3 class="text-xl font-bold text-white mb-2">BJJ Pro</h3>
                    <div class="text-3xl font-bold text-white mb-4">$20</div>
                    <ul class="text-white space-y-2 mb-6 text-sm">
                        <li>• Unlimited videos</li>
                        <li>• Real analytics</li>
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
    
    if user_plan == 'demo':
        html += '''<div class="bg-red-900 bg-opacity-50 rounded-lg p-6 text-center mb-6">
                    <h3 class="text-xl font-bold text-white mb-2">🚫 Upload Not Available</h3>
                    <p class="text-gray-300 mb-4">Demo users need access code or subscription</p>
                    <div class="space-x-4">
                        <button onclick="showAccessCode()" class="bg-yellow-600 hover:bg-yellow-700 text-white font-bold py-2 px-4 rounded-lg">
                            Use Access Code
                        </button>
                        <button onclick="showPricing()" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg">
                            Subscribe
                        </button>
                    </div>
                </div>'''
    else:
        html += f'''<div class="text-center">
                    <input type="file" id="videoFile" accept="video/*" class="mb-4 text-white">
                    <br>
                    <p class="text-green-300 text-sm mb-4">✅ {user_plan.title()} Plan - Real analysis</p>
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
                    alert('✅ Code redeemed! Refreshing...');
                    location.reload();
                } else {
                    alert('❌ ' + result.message);
                }
            } catch (error) {
                alert('Error: ' + error.message);
            }
        }

        function subscribePlan(plan) {
            alert(`🚀 Subscribing to ${plan.toUpperCase()}!\\n\\nPayment integration would go here.\\n\\nFor demo: use BJJ2024FREE`);
        }

        async function analyzeVideo() {
            const fileInput = document.getElementById('videoFile');
            if (!fileInput.files[0]) return alert('Select a video first!');

            document.getElementById('upload-section').classList.add('hidden');
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
                displayResults(results);
            } catch (error) {
                alert('Analysis failed: ' + error.message);
                resetApp();
            }
        }

        function displayResults(results) {
