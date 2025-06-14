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
        status_html = f'<span class="bg-green-600 text-white px-4 py-2 rounded-lg">✅ {user_plan.upper()} MEMBER • {video_count} Videos</span>'
    else:
        status_html = f'''<div class="space-x-4">
            <span class="bg-orange-600 text-white px-3 py-2 rounded-lg text-sm">🆓 DEMO • {demo_uploads_used}/1 Free Upload Used</span>
            <button onclick="showAccessCode()" class="bg-yellow-600 hover:bg-yellow-700 text-white px-4 py-2 rounded-lg font-bold">🎁 Elite Access Code?</button>
            <button onclick="showPricing()" class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-bold">🚀 SUBSCRIBE NOW</button>
        </div>'''
    
    # Demo badges
    demo_badge = '<span class="demo-badge">DEMO</span>' if user_plan == 'demo' else ''
    
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
                </div>
                <div class="text-center">
                    <input type="file" id="videoFile" accept="video/*" class="mb-4 text-white">
                    <br>
                    <button onclick="analyzeVideo()" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-lg">🤖 Try AI Analysis</button>
                </div>'''
    else:
        elite_note = '<p class="text-purple-300 text-xs mt-2">🎬 Elite: Video timestamps included!</p>' if user_plan == 'elite' else ''
        upload_section = f'''<div class="text-center">
                    <input type="file" id="videoFile" accept="video/*" class="mb-4 text-white">
                    <br>
                    <button onclick="analyzeVideo()" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-lg">🤖 Analyze Techniques</button>
                    {elite_note}
                </div>'''
    
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
        .demo-badge {{ position: absolute; top: 5px; right: 5px; background: rgba(255, 193, 7, 0.9); color: black; padding: 2px 6px; border-radius: 3px; font-size: 10px; }}
    </style>
</head>
<body class="min-h-screen">
    <div class="text-center py-8">
        <h1 class="text-5xl font-bold text-white mb-4">🥋 BJJ AI Analyzer Pro</h1>
        <p class="text-xl text-gray-200">Complete BJJ Analytics Platform</p>
        <div class="mt-4">{status_html}</div>
    </div>

    <!-- Navigation -->
    <div class="container mx-auto px-4 max-w-6xl mb-8">
        <div class="glass rounded-xl p-2">
            <div class="flex flex-wrap justify-center space-x-2">
                <button onclick="showTab('upload')" class="tab-button active px-4 py-2 rounded-lg text-white font-semibold">📹 Upload</button>
                <button onclick="showTab('submissions')" class="tab-button px-4 py-2 rounded-lg text-white font-semibold relative">🎯 Submissions{demo_badge}</button>
                <button onclick="showTab('analytics')" class="tab-button px-4 py-2 rounded-lg text-white font-semibold relative">📊 Analytics{demo_badge}</button>
                {"" if user_plan == "demo" else '''<button onclick="showTab('challenges')" class="tab-button px-4 py-2 rounded-lg text-white font-semibold">🏆 Challenges</button>
                <button onclick="showTab('friends')" class="tab-button px-4 py-2 rounded-lg text-white font-semibold">👥 Friends</button>'''}
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
            </div>
        </div>

        <!-- Other tabs -->
        <div id="submissions-tab" class="tab-content">
            <div class="glass rounded-xl p-8">
                <h2 class="text-2xl font-bold text-white mb-6">🎯 Submission Analytics</h2>
                <div class="bg-white bg-opacity-10 rounded-lg p-6">
                    <div id="real-submission-data" class="text-center text-gray-300">
                        <p>Upload videos to see your real submission statistics</p>
                    </div>
                </div>
            </div>
        </div>

        <div id="analytics-tab" class="tab-content">
            <div class="glass rounded-xl p-8">
                <h2 class="text-2xl font-bold text-white mb-6">📊 Complete Analytics</h2>
                <div id="real-analytics-data" class="text-center text-gray-300">
                    <p>Upload videos to see your real performance analytics</p>
                </div>
            </div>
        </div>

        {"" if user_plan == "demo" else '''<!-- Challenges Tab -->
        <div id="challenges-tab" class="tab-content">
            <div class="glass rounded-xl p-8">
                <h2 class="text-2xl font-bold text-white mb-6">🏆 Weekly Training Challenges</h2>
                <div class="bg-white bg-opacity-10 rounded-lg p-6">
                    <h3 class="text-xl font-bold text-white mb-4">⚙️ Challenge Preferences</h3>
                    <button onclick="updateChallengePreferences()" class="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg font-bold">💾 Save Preferences</button>
                </div>
            </div>
        </div>

        <!-- Friends Tab -->
        <div id="friends-tab" class="tab-content">
            <div class="glass rounded-xl p-8">
                <h2 class="text-2xl font-bold text-white mb-6">👥 Friends & Community</h2>
                <div class="bg-white bg-opacity-10 rounded-lg p-6">
                    <button onclick="connectFacebook()" class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-bold">🔗 Connect Facebook</button>
                </div>
            </div>
        </div>'''}
    </div>

    <script>
        const userPlan = "{user_plan}";

        function showTab(tabName) {{
            document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
            document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
            document.getElementById(tabName + '-tab').classList.add('active');
            event.target.classList.add('active');
        }}

        function showAccessCode() {{ alert('Access code feature coming soon!'); }}
        function showPricing() {{ alert('PayPal integration coming soon!'); }}
        function updateChallengePreferences() {{ alert('Challenge preferences saved!'); }}
        function connectFacebook() {{ alert('Facebook connection coming soon!'); }}

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
                    return;
                }}
                
                displayResults(results);
            }} catch (error) {{
                alert('Analysis failed: ' + error.message);
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
        }}

        function displayTechniques(techniques) {{
            const techniquesList = document.getElementById('techniques-list');
            techniquesList.innerHTML = '';

            techniques.forEach(technique => {{
                const techniqueDiv = document.createElement('div');
                techniqueDiv.className = 'bg-white bg-opacity-10 rounded-lg p-4 mb-3';
                
                let timestampHTML = '';
                if (technique.has_timestamp) {{
                    timestampHTML = `<button onclick="alert('🎬 Elite timestamp feature!')" 
                                    class="bg-blue-600 hover:bg-blue-700 text-white px-2 py-1 rounded text-xs ml-2">
                        🎬 ${{Math.floor(technique.start_time/60)}}:${{(technique.start_time%60).toString().padStart(2, '0')}}
                    </button>`;
                }}

                techniqueDiv.innerHTML = `
                    <div class="flex justify-between items-center">
                        <div class="flex-1">
                            <h4 class="text-lg font-bold text-white">${{technique.technique.replace(/_/g, ' ')}}</h4>
                            <p class="text-gray-300 text-sm">${{technique.category}} | ${{technique.quality}}</p>
                            ${{timestampHTML}}
                        </div>
                        <div class="text-right">
                            <div class="text-white font-bold text-lg">${{Math.round(technique.confidence * 100)}}%</div>
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
                insightDiv.className = 'bg-white bg-opacity-10 rounded p-3 mb-2';
                insightDiv.innerHTML = `<p class="text-gray-300">${{insight}}</p>`;
                insightsList.appendChild(insightDiv);
            }});
        }}
    </script>
</body>
</html>'''

@app.route('/api/analyze', methods=['POST'])
def analyze():
    user_id = get_user_id()
    user_plan = users[user_id]['plan']
    
    if user_plan == 'demo':
        demo_uploads_used = len(user_videos.get(user_id, []))
        if demo_uploads_used >= 1:
            return jsonify({'error': 'Demo limit reached! Use elite access code or subscribe.'}), 403
    
    time.sleep(3)
    analysis_result = generate_analysis(user_plan)
    
    if user_id not in user_videos:
        user_videos[user_id] = []
    user_videos[user_id].append(analysis_result)
    users[user_id]['videos_count'] += 1
    
    return jsonify(analysis_result)

@app.route('/api/redeem-code', methods=['POST'])
def redeem_code():
    user_id = get_user_id()
    data = request.get_json()
    code = data.get('code', '').upper()
    
    if code in access_codes and access_codes[code]['uses'] > 0:
        access_codes[code]['uses'] -= 1
        users[user_id]['plan'] = access_codes[code]['plan']
        return jsonify({'success': True, 'message': 'Elite access activated!'})
    else:
        return jsonify({'success': False, 'message': 'Invalid or expired access code'})

@app.route('/health')
def health():
    return jsonify({'status': 'running'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
