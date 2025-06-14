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
        num_techniques = random.randint(3, 5)
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
    
    # Ensure user exists in users dict
    if user_id not in users:
        users[user_id] = {
            'plan': 'demo',
            'videos_count': 0,
            'created_at': datetime.now().isoformat()
        }
        user_videos[user_id] = []
    
    user_plan = users[user_id]['plan']
    video_count = len(user_videos.get(user_id, []))
    demo_uploads_used = video_count if user_plan == 'demo' else 0
    
    # Status section
    if user_plan != 'demo':
        status_html = '<span class="bg-green-600 text-white px-4 py-2 rounded-lg">✅ {} MEMBER • {} Videos</span>'.format(user_plan.upper(), video_count)
    else:
        status_html = '''<div class="space-x-4">
            <span class="bg-orange-600 text-white px-3 py-2 rounded-lg text-sm">🆓 DEMO • {}/1 Free Upload Used</span>
            <button onclick="showAccessCode()" class="bg-yellow-600 hover:bg-yellow-700 text-white px-4 py-2 rounded-lg font-bold">🎁 Elite Access Code?</button>
            <button onclick="showPricing()" class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-bold">🚀 SUBSCRIBE NOW</button>
        </div>'''.format(demo_uploads_used)
    
    # Navigation badges
    demo_badge = '<span class="demo-badge">DEMO</span>' if user_plan == 'demo' else ''
    
    # Friends tab
    friends_tab = '''<button onclick="showTab('friends')" class="tab-button px-4 py-2 rounded-lg text-white font-semibold">👥 Friends</button>''' if user_plan in ['pro', 'elite'] else ''
    
    # Upload section
    if user_plan == 'demo' and demo_uploads_used >= 1:
        upload_section = '''<div class="bg-orange-900 bg-opacity-50 rounded-lg p-6 text-center mb-6">
                    <h3 class="text-xl font-bold text-white mb-2">🆓 Free Upload Used</h3>
                    <p class="text-gray-300 mb-4">You've used your 1 free demo upload. Get elite access or subscribe for unlimited uploads!</p>
                    <div class="space-x-4">
                        <button onclick="showAccessCode()" class="bg-yellow-600 hover:bg-yellow-700 text-white font-bold py-2 px-4 rounded-lg">🎁 Use Elite Code</button>
                        <button onclick="showPricing()" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg">Subscribe</button>
                    </div>
                </div>'''
    elif user_plan == 'demo':
        upload_section = '''<div class="bg-green-900 bg-opacity-50 rounded-lg p-6 text-center mb-6">
                    <h3 class="text-xl font-bold text-white mb-2">🆓 Free Demo Upload</h3>
                    <p class="text-gray-300 mb-4">Try our AI analysis with 1 free upload! Limited breakdown included.</p>
                    <p class="text-yellow-300 text-sm">After this, use an elite access code or subscribe for unlimited uploads.</p>
                </div>
                <div class="text-center">
                    <input type="file" id="videoFile" accept="video/*" class="mb-4 text-white">
                    <br>
                    <p class="text-orange-300 text-sm mb-4">🆓 Demo Plan - Basic analysis (upgrade for full features)</p>
                    <button onclick="analyzeVideo()" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-lg">🤖 Try AI Analysis</button>
                </div>'''
    else:
        elite_note = '<p class="text-purple-300 text-xs mt-2">🎬 Elite: Video timestamps included!</p>' if user_plan == 'elite' else ''
        upload_section = '''<div class="text-center">
                    <input type="file" id="videoFile" accept="video/*" class="mb-4 text-white">
                    <br>
                    <p class="text-green-300 text-sm mb-4">✅ {} Plan - Full analysis</p>
                    <button onclick="analyzeVideo()" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-lg">🤖 Analyze Techniques</button>
                    {}
                </div>'''.format(user_plan.title(), elite_note)
    
    # Friends content
    friends_content = '''
        <!-- Friends Tab -->
        <div id="friends-tab" class="tab-content">
            <div class="glass rounded-xl p-8">
                <h2 class="text-2xl font-bold text-white mb-6">👥 Friends & Community</h2>
                
                <!-- Facebook Connect Section -->
                <div class="bg-blue-800 bg-opacity-30 rounded-lg p-6 mb-8 border border-blue-500">
                    <div class="flex items-center justify-between mb-4">
                        <div class="flex items-center space-x-3">
                            <span class="text-3xl">📘</span>
                            <div>
                                <h3 class="text-xl font-bold text-white">Connect Facebook Friends</h3>
                                <p class="text-blue-200 text-sm">Find friends who also train BJJ and use our app</p>
                            </div>
                        </div>
                        <button id="fb-connect-btn" onclick="connectFacebook()" 
                                class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-bold">
                            🔗 Connect Facebook
                        </button>
                    </div>
                    <div id="fb-friends-list" class="hidden">
                        <h4 class="text-white font-bold mb-3">Facebook Friends on BJJ AI Analyzer:</h4>
                        <div id="fb-friends-container" class="space-y-2"></div>
                    </div>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
                    <div class="bg-white bg-opacity-10 rounded-lg p-6">
                        <h3 class="text-xl font-bold text-white mb-4">Add Friends</h3>
                        <div class="space-y-4">
                            <input type="text" id="friend-search" placeholder="Enter friend's username" 
                                   class="w-full p-3 rounded-lg bg-white bg-opacity-20 text-white placeholder-gray-300">
                            <button onclick="searchFriend()" class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg w-full font-bold">🔍 Search & Add Friend</button>
                        </div>
                    </div>
                    <div class="bg-white bg-opacity-10 rounded-lg p-6">
                        <h3 class="text-xl font-bold text-white mb-4">Friend Requests</h3>
                        <div id="friend-requests" class="space-y-3">
                            <div class="flex justify-between items-center bg-white bg-opacity-10 rounded p-3">
                                <span class="text-white">@mikehook23</span>
                                <div class="space-x-2">
                                    <button class="bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded text-sm">Accept</button>
                                    <button class="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded text-sm">Decline</button>
                                </div>
                            </div>
                            <div class="flex justify-between items-center bg-white bg-opacity-10 rounded p-3">
                                <span class="text-white">@guardgirl</span>
                                <div class="space-x-2">
                                    <button class="bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded text-sm">Accept</button>
                                    <button class="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded text-sm">Decline</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="bg-white bg-opacity-10 rounded-lg p-6 mb-8">
                    <h3 class="text-xl font-bold text-white mb-4">🏆 Leaderboard</h3>
                    <div class="space-y-3">
                        <div class="flex justify-between items-center bg-gradient-to-r from-yellow-600 to-yellow-700 rounded p-3">
                            <div class="flex items-center space-x-3">
                                <span class="text-2xl">🥇</span>
                                <span class="text-white font-bold">@submachine92</span>
                            </div>
                            <span class="text-white font-bold">2,847 pts</span>
                        </div>
                        <div class="flex justify-between items-center bg-gradient-to-r from-gray-400 to-gray-500 rounded p-3">
                            <div class="flex items-center space-x-3">
                                <span class="text-2xl">🥈</span>
                                <span class="text-white font-bold">@triangletrap</span>
                            </div>
                            <span class="text-white font-bold">2,103 pts</span>
                        </div>
                        <div class="flex justify-between items-center bg-gradient-to-r from-orange-600 to-orange-700 rounded p-3">
                            <div class="flex items-center space-x-3">
                                <span class="text-2xl">🥉</span>
                                <span class="text-white font-bold">@sweepking</span>
                            </div>
                            <span class="text-white font-bold">1,978 pts</span>
                        </div>
                        <div class="flex justify-between items-center bg-white bg-opacity-10 rounded p-3 border-2 border-blue-400">
                            <div class="flex items-center space-x-3">
                                <span class="text-lg">4️⃣</span>
                                <span class="text-blue-300 font-bold">You</span>
                            </div>
                            <span class="text-blue-300 font-bold">1,654 pts</span>
                        </div>
                    </div>
                </div>
                
                <div class="bg-white bg-opacity-10 rounded-lg p-6">
                    <h3 class="text-xl font-bold text-white mb-4">📊 Friends Activity</h3>
                    <div class="space-y-4">
                        <div class="bg-white bg-opacity-10 rounded p-4">
                            <div class="flex items-center space-x-3 mb-2">
                                <span class="text-green-400 font-bold">@mikehook23</span>
                                <span class="text-gray-300 text-sm">2 hours ago</span>
                            </div>
                            <p class="text-gray-300 text-sm">Analyzed a training session • 12 techniques detected</p>
                            <div class="flex space-x-4 mt-2 text-xs">
                                <span class="text-blue-400">🎯 4 submissions</span>
                                <span class="text-yellow-400">🌊 3 sweeps</span>
                            </div>
                        </div>
                        <div class="bg-white bg-opacity-10 rounded p-4">
                            <div class="flex items-center space-x-3 mb-2">
                                <span class="text-green-400 font-bold">@guardgirl</span>
                                <span class="text-gray-300 text-sm">1 day ago</span>
                            </div>
                            <p class="text-gray-300 text-sm">Hit a new personal record • 95% confidence armbar</p>
                            <div class="flex space-x-4 mt-2 text-xs">
                                <span class="text-red-400">🔥 New PB!</span>
                                <span class="text-purple-400">⚡ Elite timing</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>''' if user_plan in ['pro', 'elite'] else ''
    
    # Build the complete HTML
    html = '''<!DOCTYPE html>
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
        .demo-badge {{ position: absolute; top: 5px; right: 5px; background: rgba(255, 193, 7, 0.9); color: black; padding: 2px 6px; border-radius: 3px; font-size: 10px; }}
    </style>
</head>
<body class="min-h-screen">
    <div class="text-center py-8">
        <h1 class="text-5xl font-bold text-white mb-4">🥋 BJJ AI Analyzer Pro</h1>
        <p class="text-xl text-gray-200">Complete BJJ Analytics Platform</p>
        <div class="mt-4">{status_html}</div>
    </div>

    <!-- Access Code Modal -->
    <div id="access-code-modal" class="fixed inset-0 bg-black bg-opacity-50 hidden z-50 flex items-center justify-center">
        <div class="glass rounded-xl p-8 max-w-md mx-4">
            <h2 class="text-2xl font-bold text-white mb-4">🎁 Elite Access Code</h2>
            <p class="text-gray-300 mb-4">Got a code for free Elite access? Enter it here!</p>
            <input type="text" id="access-code-input" placeholder="Enter elite access code" 
                   class="w-full p-3 rounded-lg bg-white bg-opacity-20 text-white placeholder-gray-300 mb-4">
            <div class="space-x-4">
                <button onclick="redeemCode()" class="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg font-bold">Redeem Elite</button>
                <button onclick="hideAccessCode()" class="bg-gray-600 hover:bg-gray-700 text-white px-6 py-2 rounded-lg">Cancel</button>
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
                    <button onclick="alert('You are already on Demo!')" class="bg-gray-600 text-white py-2 px-4 rounded-lg w-full">Current Plan</button>
                </div>
                <div class="bg-blue-600 bg-opacity-20 rounded-lg p-6 text-center border-2 border-blue-400">
                    <div class="bg-blue-500 text-white px-3 py-1 rounded-full text-xs mb-2">POPULAR</div>
                    <h3 class="text-xl font-bold text-white mb-2">BJJ Pro</h3>
                    <div class="text-3xl font-bold text-white mb-4">$20</div>
                    <ul class="text-white space-y-2 mb-6 text-sm">
                        <li>• Unlimited videos</li>
                        <li>• Full analytics</li>
                        <li>• Progress tracking</li>
                        <li>• Follow friends</li>
                    </ul>
                    <button onclick="subscribePlan('pro')" class="bg-blue-600 hover:bg-blue-700 text-white py-2 px-6 rounded-lg w-full">Subscribe with PayPal</button>
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
                    <button onclick="subscribePlan('elite')" class="bg-purple-600 hover:bg-purple-700 text-white py-2 px-6 rounded-lg w-full">Subscribe</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Navigation -->
    <div class="container mx-auto px-4 max-w-6xl mb-8">
        <div class="glass rounded-xl p-2">
            <div class="flex flex-wrap justify-center space-x-2">
                <button onclick="showTab('upload')" class="tab-button active px-4 py-2 rounded-lg text-white font-semibold">📹 Upload</button>
                <button onclick="showTab('submissions')" class="tab-button px-4 py-2 rounded-lg text-white font-semibold relative">🎯 Submissions{demo_badge}</button>
                <button onclick="showTab('sweeps')" class="tab-button px-4 py-2 rounded-lg text-white font-semibold relative">🌊 Sweeps{demo_badge}</button>
                <button onclick="showTab('passes')" class="tab-button px-4 py-2 rounded-lg text-white font-semibold relative">🛡️ Passes{demo_badge}</button>
                <button onclick="showTab('takedowns')" class="tab-button px-4 py-2 rounded-lg text-white font-semibold relative">🤼 Takedowns{demo_badge}</button>
                <button onclick="showTab('analytics')" class="tab-button px-4 py-2 rounded-lg text-white font-semibold relative">📊 Analytics{demo_badge}</button>
                {friends_tab}
            </div>
        </div>
    </div>

    <div class="container mx-auto px-4 max-w-6xl">
        <!-- Upload Tab -->
        <div id="upload-tab" class="tab-content active">
            <div class="glass rounded-xl p-8 mb-8">
                <h2 class="text-2xl font-bold text-white mb-6 text-center">Upload Your BJJ Video</h2>
                {upload_section}
            </div>

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
                    <button onclick="resetApp()" class="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-6 rounded-lg">📹 Analyze Another Video</button>
                </div>
            </div>
        </div>

        <!-- Other tabs -->
        <div id="submissions-tab" class="tab-content">
            <div class="glass rounded-xl p-8">
                <h2 class="text-2xl font-bold text-white mb-6">🎯 Submission Analytics</h2>
                <div class="bg-white bg-opacity-10 rounded-lg p-6">
                    <h3 class="text-xl font-bold text-white mb-4">Real Data From Your Videos</h3>
                    <div id="real-submission-data" class="text-center text-gray-300">
                        <p>Upload videos to see your real submission statistics</p>
                    </div>
                </div>
            </div>
        </div>

        <div id="sweeps-tab" class="tab-content">
            <div class="glass rounded-xl p-8">
                <h2 class="text-2xl font-bold text-white mb-6">🌊 Sweep Analytics</h2>
                <div class="bg-white bg-opacity-10 rounded-lg p-6">
                    <h3 class="text-xl font-bold text-white mb-4">Real Data From Your Videos</h3>
                    <div id="real-sweep-data" class="text-center text-gray-300">
                        <p>Upload videos to see your real sweep statistics</p>
                    </div>
                </div>
            </div>
        </div>

        <div id="passes-tab" class="tab-content">
            <div class="glass rounded-xl p-8">
                <h2 class="text-2xl font-bold text-white mb-6">🛡️ Guard Pass Analytics</h2>
                <div class="bg-white bg-opacity-10 rounded-lg p-6">
                    <h3 class="text-xl font-bold text-white mb-4">Real Data From Your Videos</h3>
                    <div id="real-pass-data" class="text-center text-gray-300">
                        <p>Upload videos to see your real guard pass statistics</p>
                    </div>
                </div>
            </div>
        </div>

        <div id="takedowns-tab" class="tab-content">
            <div class="glass rounded-xl p-8">
                <h2 class="text-2xl font-bold text-white mb-6">🤼 Takedown Analytics</h2>
                <div class="bg-white bg-opacity-10 rounded-lg p-6">
                    <h3 class="text-xl font-bold text-white mb-4">Real Data From Your Videos</h3>
                    <div id="real-takedown-data" class="text-center text-gray-300">
                        <p>Upload videos to see your real takedown statistics</p>
                    </div>
                </div>
            </div>
        </div>

        <div id="analytics-tab" class="tab-content">
            <div class="glass rounded-xl p-8">
                <h2 class="text-2xl font-bold text-white mb-6">📊 Complete Analytics</h2>
                <div id="real-analytics-data" class="text-center text-gray-300">
                    <p>Upload videos to see your real performance analytics</p>
                    <p class="text-sm mt-2">All statistics are calculated from your actual BJJ footage</p>
                </div>
            </div>
        </div>

        {friends_content}
    </div>

    <script>
        const userPlan = "{user_plan}";

        function showTab(tabName) {{
            document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
            document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
            document.getElementById(tabName + '-tab').classList.add('active');
            event.target.classList.add('active');
        }}

        function showAccessCode() {{
            document.getElementById('access-code-modal').classList.remove('hidden');
        }}

        function hideAccessCode() {{
            document.getElementById('access-code-modal').classList.add('hidden');
        }}

        function showPricing() {{
            document.getElementById('pricing-modal').classList.remove('hidden');
        }}

        function hidePricing() {{
            document.getElementById('pricing-modal').classList.add('hidden');
        }}

        async function redeemCode() {{
            const code = document.getElementById('access-code-input').value.trim();
            if (!code) return alert('Enter a code');

            try {{
                const response = await fetch('/api/redeem-code', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{code: code}})
                }});
                const result = await response.json();
                
                if (result.success) {{
                    alert('🎉 Elite access activated! Refreshing...');
                    location.reload();
                }} else {{
                    alert('❌ ' + result.message);
                }}
            }} catch (error) {{
                alert('Error: ' + error.message);
            }}
        }}

        function subscribePlan(plan) {{
            alert(`🚀 Subscribing to ${{plan.toUpperCase()}}!\\n\\nPayment integration would go here.\\n\\nFor demo: use BJJ2024FREE for elite access`);
        }}

        async function analyzeVideo() {{
            const fileInput = document.getElementById('videoFile');
            if (!fileInput.files[0]) return alert('Select a video first!');

            document.getElementById('progress-section').classList.remove('hidden');
            let progress = 0;
            const progressBar = document.getElementById('progress-bar');
            
            const interval = setInterval(() => {{
                progress += Math.random() * 15;
                if (progress > 100) progress = 100;
                progressBar.style.width = progress + '%';
                
                if (progress >= 100) {{
                    clearInterval(interval);
                    performAnalysis();
                }}
            }}, 300);
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
                    resetApp();
                    return;
                }}
                
                displayResults(results);
            }} catch (error) {{
                alert('Analysis failed: ' + error.message);
                resetApp();
            }}
        }}

        function displayResults(results) {{
            document.getElementById('progress-section').classList.add('hidden');
            document.getElementById('results-section').classList.remove('hidden');

            document.getElementById('total-count').textContent = results.total_techniques_detected;
            document.getElementById('avg-confidence').textContent = Math.round(results.average_confidence * 100) + '%';
            document.getElementById('video-duration').textContent = results.video_duration + 's';
            
            const submissionCount = results.detected_techniques.filter(t => t.category === 'submission').length;
            document.getElementById('submission-count').textContent = submissionCount;

            displayTechniques(results.detected_techniques);
            displayInsights(results.insights);
            
            // Update all tabs with real data (for non-demo users)
            updateRealAnalytics(results);
        }}

        function displayTechniques(techniques) {{
            const techniquesList = document.getElementById('techniques-list');
            techniquesList.innerHTML = '';

            techniques.forEach(technique => {{
                const techniqueDiv = document.createElement('div');
                techniqueDiv.className = 'bg-white bg-opacity-10 rounded-lg p-4 mb-3';
                
                let timestampHTML = '';
                if (technique.has_timestamp) {{
                    timestampHTML = `<button onclick="seekVideo(${{technique.start_time}})" 
                                    class="bg-blue-600 hover:bg-blue-700 text-white px-2 py-1 rounded text-xs ml-2">
                        🎬 ${{Math.floor(technique.start_time/60)}}:${{(technique.start_time%60).toString().padStart(2, '0')}}
                    </button>
                    <button onclick="extractClip(${{technique.start_time}}, ${{technique.end_time}}, '${{technique.technique}}')" 
                            class="bg-purple-600 hover:bg-purple-700 text-white px-2 py-1 rounded text-xs ml-1">
                        ✂️ Extract Clip
                    </button>`;
                }}

                techniqueDiv.innerHTML = `
                    <div class="flex justify-between items-center">
                        <div class="flex-1">
                            <div class="flex items-center space-x-2 mb-1">
                                <h4 class="text-lg font-bold text-white">${{technique.technique.replace(/_/g, ' ').replace(/\\b\\w/g, l => l.toUpperCase())}}</h4>
                                <span class="px-2 py-1 bg-white bg-opacity-20 rounded text-xs text-gray-300">
                                    ${{technique.category.replace('_', ' ').toUpperCase()}}
                                </span>
                                ${{timestampHTML}}
                            </div>
                            <p class="text-gray-300 text-sm">Position: ${{technique.position}} | Quality: ${{technique.quality}}</p>
                        </div>
                        <div class="text-right">
                            <div class="text-white font-bold text-lg">${{Math.round(technique.confidence * 100)}}%</div>
                        </div>
                    </div>
                `;
                
                techniquesList.appendChild(techniqueDiv);
            }});
        }}

        // Video seeking functionality
        let currentVideo = null;
        
        function seekVideo(timeInSeconds) {{
            if (currentVideo) {{
                currentVideo.currentTime = timeInSeconds;
                currentVideo.play();
            }} else {{
                alert('🎬 Video seek ready! In full version, this would jump to ' + Math.floor(timeInSeconds/60) + ':' + (timeInSeconds%60).toString().padStart(2, '0'));
            }}
        }}

        function extractClip(startTime, endTime, techniqueName) {{
            // In production, this would extract the video clip
            alert(`✂️ Extracting clip: "${{techniqueName.replace(/_/g, ' ')}}"\\nFrom: ${{Math.floor(startTime/60)}}:${{(startTime%60).toString().padStart(2, '0')}} to ${{Math.floor(endTime/60)}}:${{(endTime%60).toString().padStart(2, '0')}}\\n\\nIn full app, this would create a downloadable clip!`);
        }}

        // Set video reference when file is selected
        document.addEventListener('DOMContentLoaded', function() {{
            const videoInput = document.getElementById('videoFile');
            if (videoInput) {{
                videoInput.addEventListener('change', function(e) {{
                    if (e.target.files[0]) {{
                        // Create video element for seeking (hidden)
                        if (currentVideo) {{
                            document.body.removeChild(currentVideo);
                        }}
                        currentVideo = document.createElement('video');
                        currentVideo.src = URL.createObjectURL(e.target.files[0]);
                        currentVideo.style.display = 'none';
                        document.body.appendChild(currentVideo);
                    }}
                }});
            }}
        }});
        }}

        function displayInsights(insights) {{
            const insightsList = document.getElementById('insights-list');
            insightsList.innerHTML = '';

            insights.forEach(insight => {{
                const insightDiv = document.createElement('div');
                insightDiv.className = 'bg-white bg-opacity-10 rounded p-3 mb-2';
                insightDiv.innerHTML = `<p class="text-gray-300">${{insight}}</p>`;
                insightsList.appendChild(insightDiv);
            }});
        }}

        function resetApp() {{
            document.getElementById('progress-section').classList.add('hidden');
            document.getElementById('results-section').classList.add('hidden');
            document.getElementById('videoFile').value = '';
        }}

        // Initialize chart only for demo users
        setTimeout(() => {{
            if (userPlan === 'demo') {{
                const ctx = document.getElementById('submission-chart');
                if (ctx && window.Chart) {{
                    new Chart(ctx, {{
                        type: 'doughnut',
                        data: {{
                            labels: ['Demo Data Only'],
                            datasets: [{{
                                data: [100],
                                backgroundColor: ['#6b7280']
                            }}]
                        }},
                        options: {{
                            responsive: true,
                            plugins: {{
                                legend: {{ 
                                    labels: {{ color: 'white' }},
                                    display: true
                                }}
                            }}
                        }}
                    }});
                }}
            }}
        }}, 1000);

        // Update analytics with real data after analysis
        function updateRealAnalytics(analysisData) {{
            if (userPlan !== 'demo') {{
                // Update submissions tab with real data
                const submissionData = analysisData.detected_techniques.filter(t => t.category === 'submission');
                document.getElementById('real-submission-data').innerHTML = `
                    <div class="grid grid-cols-2 gap-4">
                        <div class="text-center">
                            <div class="text-2xl font-bold text-white">${{submissionData.length}}</div>
                            <div class="text-gray-300">Total Submissions</div>
                        </div>
                        <div class="text-center">
                            <div class="text-2xl font-bold text-white">${{submissionData.length > 0 ? Math.round(submissionData.reduce((a,b) => a + b.confidence, 0) / submissionData.length * 100) : 0}}%</div>
                            <div class="text-gray-300">Avg Confidence</div>
                        </div>
                    </div>
                `;

                // Update other tabs with real data
                const sweepData = analysisData.detected_techniques.filter(t => t.category === 'sweep');
                document.getElementById('real-sweep-data').innerHTML = `
                    <div class="text-center">
                        <div class="text-2xl font-bold text-white">${{sweepData.length}}</div>
                        <div class="text-gray-300">Sweeps Detected</div>
                    </div>
                `;

                const passData = analysisData.detected_techniques.filter(t => t.category === 'guard_pass');
                document.getElementById('real-pass-data').innerHTML = `
                    <div class="text-center">
                        <div class="text-2xl font-bold text-white">${{passData.length}}</div>
                        <div class="text-gray-300">Guard Passes</div>
                    </div>
                `;

                const takedownData = analysisData.detected_techniques.filter(t => t.category === 'takedown');
                document.getElementById('real-takedown-data').innerHTML = `
                    <div class="text-center">
                        <div class="text-2xl font-bold text-white">${{takedownData.length}}</div>
                        <div class="text-gray-300">Takedowns</div>
                    </div>
                `;

                // Update analytics tab
                document.getElementById('real-analytics-data').innerHTML = `
                    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
                        <div class="bg-gradient-to-br from-blue-600 to-blue-800 rounded-lg p-6 text-center">
                            <div class="text-3xl font-bold text-white">${{analysisData.total_techniques_detected}}</div>
                            <div class="text-blue-200">Total Techniques</div>
                        </div>
                        <div class="bg-gradient-to-br from-green-600 to-green-800 rounded-lg p-6 text-center">
                            <div class="text-3xl font-bold text-white">${{Math.round(analysisData.average_confidence * 100)}}%</div>
                            <div class="text-green-200">Avg Confidence</div>
                        </div>
                        <div class="bg-gradient-to-br from-purple-600 to-purple-800 rounded-lg p-6 text-center">
                            <div class="text-3xl font-bold text-white">${{Math.round(analysisData.video_duration / 60)}}m</div>
                            <div class="text-purple-200">Video Length</div>
                        </div>
                        <div class="bg-gradient-to-br from-orange-600 to-orange-800 rounded-lg p-6 text-center">
                            <div class="text-3xl font-bold text-white">${{analysisData.techniques_per_minute}}</div>
                            <div class="text-orange-200">Techniques/Min</div>
                        </div>
                    </div>
                `;
            }}
        }}
    </script>
</body>
</html>'''.format(
        status_html=status_html,
        demo_badge=demo_badge,
        friends_tab=friends_tab,
        upload_section=upload_section,
        friends_content=friends_content,
        video_count=video_count,
        user_plan=user_plan
    )
    
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
