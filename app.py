from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import json
from datetime import datetime, timedelta
import time
import random
import uuid
import hashlib

app = Flask(__name__)
app.secret_key = 'bjj-ai-secret-key-2024'

# Database simulation (use real database in production)
users_db = {}
user_videos_db = {}
access_codes_db = {}
subscriptions_db = {}

class SubscriptionManager:
    def __init__(self):
        self.plans = {
            'free': {
                'name': 'Free Monthly',
                'price': 0,
                'monthly_videos': 1,
                'features': [
                    'View demo analytics',
                    '1 video analysis per month',
                    'Basic technique detection',
                    'Limited insights'
                ],
                'video_timestamps': False,
                'real_analytics': False
            },
            'pro': {
                'name': 'BJJ Pro',
                'price': 20.00,
                'monthly_videos': -1,  # Unlimited
                'features': [
                    'Unlimited video analysis',
                    'Real personal analytics',
                    'Progress tracking over time',
                    'Advanced training recommendations',
                    'Technique success rate tracking',
                    'Export analysis reports'
                ],
                'video_timestamps': False,
                'real_analytics': True
            },
            'elite': {
                'name': 'Elite Competitor',
                'price': 50.00,
                'monthly_videos': -1,  # Unlimited
                'features': [
                    'Everything in Pro',
                    'Video timestamp linking',
                    'Frame-by-frame technique breakdown',
                    'Competition analysis tools',
                    'Opponent scouting reports',
                    'Advanced biomechanics insights',
                    'Priority customer support',
                    'Beta feature access'
                ],
                'video_timestamps': True,
                'real_analytics': True
            }
        }
        
        # Generate some access codes for free accounts
        self.generate_access_codes()
    
    def generate_access_codes(self):
        """Generate access codes for free accounts"""
        codes = [
            'BJJ2024FREE', 'GUARD2024', 'SWEEP2024', 'SUBMIT2024', 'ESCAPE2024',
            'MOUNT2024', 'PASS2024', 'CHOKE2024', 'JOINT2024', 'FLOW2024'
        ]
        
        for code in codes:
            access_codes_db[code] = {
                'plan': 'free',
                'uses_remaining': 100,  # Each code can be used 100 times
                'created_at': datetime.now().isoformat(),
                'expires_at': (datetime.now() + timedelta(days=365)).isoformat()
            }
    
    def validate_access_code(self, code):
        """Validate and use an access code"""
        if code.upper() in access_codes_db:
            code_data = access_codes_db[code.upper()]
            if code_data['uses_remaining'] > 0:
                expires_at = datetime.fromisoformat(code_data['expires_at'])
                if datetime.now() < expires_at:
                    access_codes_db[code.upper()]['uses_remaining'] -= 1
                    return code_data['plan']
        return None
    
    def get_user_plan(self, user_id):
        if user_id in users_db:
            return users_db[user_id].get('plan', 'demo')
        return 'demo'
    
    def get_user_subscription(self, user_id):
        return subscriptions_db.get(user_id, {})
    
    def is_subscriber(self, user_id):
        plan = self.get_user_plan(user_id)
        return plan in ['free', 'pro', 'elite']
    
    def can_upload_video(self, user_id):
        if not user_id:
            return False, "Please create an account first"
        
        plan = self.get_user_plan(user_id)
        
        if plan == 'demo':
            return False, "Please use an access code or subscribe to upload videos"
        
        if plan == 'free':
            # Check monthly limit
            user_videos = user_videos_db.get(user_id, [])
            current_month = datetime.now().strftime('%Y-%m')
            monthly_uploads = [v for v in user_videos if v['timestamp'].startswith(current_month)]
            
            if len(monthly_uploads) >= 1:
                return False, "Free plan allows 1 video per month. Upgrade to Pro for unlimited uploads!"
            
            return True, "Free monthly upload available"
        
        return True, f"{plan.title()} plan - unlimited uploads"
    
    def has_video_timestamps(self, user_id):
        """Check if user has access to video timestamp feature"""
        plan = self.get_user_plan(user_id)
        return self.plans.get(plan, {}).get('video_timestamps', False)
    
    def subscribe_user(self, user_id, plan):
        """Subscribe user to a plan"""
        if plan in self.plans:
            users_db[user_id]['plan'] = plan
            subscriptions_db[user_id] = {
                'plan': plan,
                'subscribed_at': datetime.now().isoformat(),
                'next_billing': (datetime.now() + timedelta(days=30)).isoformat(),
                'status': 'active'
            }
            return True
        return False

subscription_manager = SubscriptionManager()

class BJJAnalyzer:
    def __init__(self):
        # Mock data for demo users
        self.demo_data = {
            'submission_success_rates': {
                'armbar_from_guard': 87, 'triangle_choke': 72, 'rear_naked_choke': 95,
                'kimura': 65, 'americana': 58, 'heel_hook': 81, 'ankle_lock': 73
            },
            'sweep_success_rates': {
                'tripod_sweep': 92, 'scissor_sweep': 68, 'butterfly_sweep': 81,
                'flower_sweep': 55, 'de_la_riva_sweep': 73, 'x_guard_sweep': 78
            },
            'guard_pass_success_rates': {
                'knee_cut_pass': 82, 'toreando_pass': 75, 'stack_pass': 60,
                'leg_drag_pass': 88, 'over_under_pass': 71
            },
            'takedown_success_rates': {
                'double_leg_takedown': 70, 'single_leg_takedown': 55, 'hip_toss': 45,
                'foot_sweep': 38, 'guard_pull': 85
            }
        }
    
    def analyze_video_demo(self):
        """Generate demo analysis for non-subscribers"""
        demo_techniques = [
            {'technique': 'armbar_from_guard', 'category': 'submission', 'confidence': 0.87, 'start_time': 15, 'end_time': 25, 'quality': 'good', 'position': 'guard'},
            {'technique': 'triangle_choke', 'category': 'submission', 'confidence': 0.82, 'start_time': 35, 'end_time': 45, 'quality': 'excellent', 'position': 'guard'},
            {'technique': 'tripod_sweep', 'category': 'sweep', 'confidence': 0.92, 'start_time': 45, 'end_time': 55, 'quality': 'excellent', 'position': 'guard'},
            {'technique': 'knee_cut_pass', 'category': 'guard_pass', 'confidence': 0.76, 'start_time': 65, 'end_time': 75, 'quality': 'good', 'position': 'guard'}
        ]
        
        return {
            'total_techniques_detected': len(demo_techniques),
            'detected_techniques': demo_techniques,
            'video_duration': 120,
            'techniques_per_minute': 2.0,
            'average_confidence': 0.84,
            'analysis_timestamp': datetime.now().isoformat(),
            'is_demo_data': True,
            'athlete_stats': self.demo_data,
            'insights': ['🎭 This is demo data - subscribe to see your real analysis!', '🔓 Upgrade to unlock personalized insights']
        }
    
    def analyze_video_real(self, user_id, video_file, include_timestamps=False):
        """Perform real analysis for subscribers"""
        time.sleep(4)  # Simulate AI processing
        
        # Generate realistic analysis
        detected_techniques = []
        
        technique_pool = {
            'submission': ['armbar_from_guard', 'triangle_choke', 'rear_naked_choke', 'kimura', 'heel_hook', 'ankle_lock'],
            'sweep': ['tripod_sweep', 'scissor_sweep', 'butterfly_sweep', 'flower_sweep', 'de_la_riva_sweep'],
            'guard_pass': ['knee_cut_pass', 'toreando_pass', 'leg_drag_pass', 'stack_pass', 'over_under_pass'],
            'takedown': ['double_leg_takedown', 'single_leg_takedown', 'hip_toss', 'foot_sweep', 'guard_pull']
        }
        
        video_duration = random.randint(180, 420)  # 3-7 minutes
        num_techniques = random.randint(4, 12)
        
        for i in range(num_techniques):
            category = random.choice(list(technique_pool.keys()))
            technique = random.choice(technique_pool[category])
            
            start_time = random.randint(10, video_duration - 30)
            end_time = start_time + random.randint(8, 25)
            
            technique_data = {
                'technique': technique,
                'category': category,
                'confidence': round(random.uniform(0.65, 0.98), 2),
                'start_time': start_time,
                'end_time': end_time,
                'quality': random.choice(['excellent', 'good', 'fair']),
                'position': random.choice(['guard', 'mount', 'side_control', 'standing', 'back_control'])
            }
            
            # Add video timestamps for Elite subscribers
            if include_timestamps:
                technique_data['video_timestamp'] = {
                    'start_url': f"#t={start_time}",
                    'end_url': f"#t={end_time}",
                    'thumbnail_time': start_time + 3
                }
            
            detected_techniques.append(technique_data)
        
        # Store analysis for user
        if user_id not in user_videos_db:
            user_videos_db[user_id] = []
        
        analysis_result = {
            'id': str(uuid.uuid4()),
            'timestamp': datetime.now().isoformat(),
            'filename': video_file.filename if hasattr(video_file, 'filename') else 'video.mp4',
            'total_techniques_detected': len(detected_techniques),
            'detected_techniques': detected_techniques,
            'video_duration': video_duration,
            'techniques_per_minute': round(len(detected_techniques) / (video_duration / 60), 1),
            'average_confidence': round(sum(t['confidence'] for t in detected_techniques) / len(detected_techniques), 2),
            'is_demo_data': False,
            'has_timestamps': include_timestamps
        }
        
        user_videos_db[user_id].append(analysis_result)
        
        # Calculate real user stats
        real_stats = self.calculate_real_user_stats(user_id)
        analysis_result['athlete_stats'] = real_stats
        analysis_result['insights'] = self.generate_real_insights(detected_techniques, real_stats)
        
        return analysis_result
    
    def calculate_real_user_stats(self, user_id):
        """Calculate stats from user's actual uploaded videos"""
        user_videos = user_videos_db.get(user_id, [])
        
        if not user_videos:
            return {'message': 'No data yet - upload more videos to see your personal stats!'}
        
        # Aggregate all techniques from user's videos
        all_techniques = []
        for video in user_videos:
            all_techniques.extend(video['detected_techniques'])
        
        # Calculate real success rates
        stats = {
            'submission_success_rates': {},
            'sweep_success_rates': {},
            'guard_pass_success_rates': {},
            'takedown_success_rates': {}
        }
        
        category_mapping = {
            'submission': 'submission_success_rates',
            'sweep': 'sweep_success_rates',
            'guard_pass': 'guard_pass_success_rates',
            'takedown': 'takedown_success_rates'
        }
        
        # Group techniques by category and calculate averages
        for technique in all_techniques:
            if technique['category'] in category_mapping:
                stat_key = category_mapping[technique['category']]
                tech_name = technique['technique']
                
                if tech_name not in stats[stat_key]:
                    stats[stat_key][tech_name] = []
                
                # Use confidence as success rate proxy
                stats[stat_key][tech_name].append(technique['confidence'] * 100)
        
        # Average the success rates
        for category in stats:
            for technique in stats[category]:
                if stats[category][technique]:
                    avg_rate = sum(stats[category][technique]) / len(stats[category][technique])
                    stats[category][technique] = round(avg_rate)
        
        stats['total_videos_analyzed'] = len(user_videos)
        stats['total_techniques_detected'] = len(all_techniques)
        
        return stats
    
    def generate_real_insights(self, techniques, stats):
        """Generate insights from real user data"""
        insights = []
        
        # Technique diversity
        unique_techniques = set(t['technique'] for t in techniques)
        if len(unique_techniques) >= 6:
            insights.append("🎯 Excellent technique diversity! You're showing a well-rounded game.")
        
        # Quality analysis
        excellent_techniques = [t for t in techniques if t['quality'] == 'excellent']
        if len(excellent_techniques) >= 3:
            insights.append("🔥 High execution quality! Multiple excellent technique demonstrations.")
        
        # Category analysis
        submissions = [t for t in techniques if t['category'] == 'submission']
        if len(submissions) >= 4:
            insights.append("🎯 Submission-focused session! You're actively hunting for finishes.")
        
        # Confidence analysis
        high_confidence = [t for t in techniques if t['confidence'] > 0.85]
        if len(high_confidence) >= 4:
            insights.append("📈 Consistent high-level execution detected across multiple techniques.")
        
        return insights

analyzer = BJJAnalyzer()

def get_user_id():
    """Get or create user session"""
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
        users_db[session['user_id']] = {
            'created_at': datetime.now().isoformat(),
            'plan': 'demo',  # Start as demo user
            'last_activity': datetime.now().isoformat()
        }
    return session['user_id']

@app.route('/')
def home():
    user_id = get_user_id()
    user_plan = subscription_manager.get_user_plan(user_id)
    is_subscriber = subscription_manager.is_subscriber(user_id)
    can_upload, upload_message = subscription_manager.can_upload_video(user_id)
    has_timestamps = subscription_manager.has_video_timestamps(user_id)
    
    # Get user's video count
    user_videos = user_videos_db.get(user_id, [])
    video_count = len(user_videos)
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BJJ AI Analyzer Pro</title>
    
    <!-- PWA Meta Tags for Mobile App -->
    <meta name="theme-color" content="#667eea">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="BJJ AI Analyzer">
    
    <!-- PWA Manifest -->
    <link rel="manifest" href="/manifest.json">
    
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    <style>
        body {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }}
        .glass {{ background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); }}
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}
        .tab-button.active {{ background: rgba(255, 255, 255, 0.2); }}
        .pulse {{ animation: pulse 2s infinite; }}
        @keyframes pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.5; }} }}
        .demo-badge {{ position: absolute; top: 10px; right: 10px; background: rgba(255, 193, 7, 0.9); color: black; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }}
        .video-timestamp {{ cursor: pointer; color: #3b82f6; text-decoration: underline; }}
        .video-timestamp:hover {{ color: #1d4ed8; }}
    </style>
</head>
<body class="min-h-screen">
    <!-- Header -->
    <div class="text-center py-8">
        <h1 class="text-5xl font-bold text-white mb-4">🥋 BJJ AI Analyzer Pro</h1>
        <p class="text-xl text-gray-200">Complete BJJ Analytics Platform</p>
        
        <!-- User Status -->
        <div class="mt-4 space-y-2">
            <div class="flex justify-center items-center space-x-4">
                {"✅" if is_subscriber else "👀"} 
                <span class="text-lg font-bold text-white">
                    {user_plan.upper().replace("_", " ")} {"MEMBER" if is_subscriber else "DEMO"}
                </span>
                {f"• {video_count} Videos Analyzed" if video_count > 0 else ""}
            </div>

            <div id="progress-section" class="glass rounded-xl p-6 mb-8 hidden">
                <h3 class="text-xl font-bold text-white mb-4">🔍 Analyzing Your Video...</h3>
                <div class="w-full bg-gray-700 rounded-full h-4 mb-4">
                    <div id="progress-bar" class="bg-blue-600 h-4 rounded-full transition-all duration-500" style="width: 0%"></div>
                </div>
                <p class="text-gray-300 text-center">
                    <span class="pulse">🧠</span> AI is detecting BJJ techniques...
                </p>
            </div>

            <div id="results-section" class="glass rounded-xl p-8 mb-8 hidden">
                <h3 class="text-2xl font-bold text-white mb-6">📊 Analysis Results</h3>
                
                <!-- Quick Stats -->
                <div class="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
                    <div class="bg-white bg-opacity-20 rounded-lg p-4 text-center">
                        <div class="text-2xl font-bold text-white" id="total-count">0</div>
                        <div class="text-gray-300 text-sm">Techniques</div>
                    </div>
                    <div class="bg-white bg-opacity-20 rounded-lg p-4 text-center">
                        <div class="text-2xl font-bold text-white" id="avg-confidence">0%</div>
                        <div class="text-gray-300 text-sm">Avg Confidence</div>
                    </div>
                    <div class="bg-white bg-opacity-20 rounded-lg p-4 text-center">
                        <div class="text-2xl font-bold text-white" id="video-length">0s</div>
                        <div class="text-gray-300 text-sm">Duration</div>
                    </div>
                    <div class="bg-white bg-opacity-20 rounded-lg p-4 text-center">
                        <div class="text-2xl font-bold text-white" id="techniques-per-min">0</div>
                        <div class="text-gray-300 text-sm">Per Minute</div>
                    </div>
                    <div class="bg-white bg-opacity-20 rounded-lg p-4 text-center">
                        <div class="text-2xl font-bold text-white" id="submission-count">0</div>
                        <div class="text-gray-300 text-sm">Submissions</div>
                    </div>
                </div>

                <!-- Techniques Timeline -->
                <div id="techniques-list" class="space-y-4 mb-6"></div>
                
                <!-- Insights -->
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
            <div class="glass rounded-xl p-8 relative">
                {'' if is_subscriber else '<div class="demo-badge">DEMO DATA</div>'}
                <h2 class="text-2xl font-bold text-white mb-6">🎯 Submission Analytics</h2>
                
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    <div class="bg-white bg-opacity-10 rounded-lg p-6">
                        <h3 class="text-xl font-bold text-white mb-4">Your Success Rates</h3>
                        <canvas id="submission-success-chart" width="400" height="300"></canvas>
                    </div>
                    
                    <div class="bg-white bg-opacity-10 rounded-lg p-6">
                        <h3 class="text-xl font-bold text-white mb-4">Most Vulnerable To</h3>
                        <div class="space-y-3">
                            <div class="flex justify-between items-center">
                                <span class="text-gray-300">Heel Hook</span>
                                <div class="flex items-center">
                                    <div class="w-24 h-3 bg-gray-700 rounded-full mr-2">
                                        <div class="h-3 bg-red-500 rounded-full" style="width: 67%"></div>
                                    </div>
                                    <span class="text-red-400 font-bold">67%</span>
                                </div>
                            </div>
                            <div class="flex justify-between items-center">
                                <span class="text-gray-300">Triangle Choke</span>
                                <div class="flex items-center">
                                    <div class="w-24 h-3 bg-gray-700 rounded-full mr-2">
                                        <div class="h-3 bg-yellow-500 rounded-full" style="width: 45%"></div>
                                    </div>
                                    <span class="text-yellow-400 font-bold">45%</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Other tabs with similar demo badges -->
        <div id="sweeps-tab" class="tab-content">
            <div class="glass rounded-xl p-8 relative">
                {'' if is_subscriber else '<div class="demo-badge">DEMO DATA</div>'}
                <h2 class="text-2xl font-bold text-white mb-6">🌊 Sweep Analytics</h2>
                <div class="bg-white bg-opacity-10 rounded-lg p-6">
                    <h3 class="text-xl font-bold text-white mb-4">Your Best Sweeps</h3>
                    <canvas id="sweep-success-chart" width="400" height="300"></canvas>
                </div>
            </div>
        </div>

        <div id="passes-tab" class="tab-content">
            <div class="glass rounded-xl p-8 relative">
                {'' if is_subscriber else '<div class="demo-badge">DEMO DATA</div>'}
                <h2 class="text-2xl font-bold text-white mb-6">🛡️ Guard Pass Analytics</h2>
                <div class="bg-white bg-opacity-10 rounded-lg p-6">
                    <h3 class="text-xl font-bold text-white mb-4">Your Passing Success</h3>
                    <canvas id="pass-success-chart" width="400" height="300"></canvas>
                </div>
            </div>
        </div>

        <div id="takedowns-tab" class="tab-content">
            <div class="glass rounded-xl p-8 relative">
                {'' if is_subscriber else '<div class="demo-badge">DEMO DATA</div>'}
                <h2 class="text-2xl font-bold text-white mb-6">🤼 Takedown Analytics</h2>
                <div class="bg-white bg-opacity-10 rounded-lg p-6">
                    <h3 class="text-xl font-bold text-white mb-4">Your Takedown Success</h3>
                    <canvas id="takedown-success-chart" width="400" height="300"></canvas>
                </div>
            </div>
        </div>

        <div id="analytics-tab" class="tab-content">
            <div class="glass rounded-xl p-8 relative">
                {'' if is_subscriber else '<div class="demo-badge">DEMO DATA</div>'}
                <h2 class="text-2xl font-bold text-white mb-6">📊 Complete Analytics Dashboard</h2>
                
                <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                    <div class="bg-gradient-to-br from-blue-600 to-blue-800 rounded-lg p-6 text-center">
                        <div class="text-3xl font-bold text-white">{"A-" if is_subscriber else "B+"}</div>
                        <div class="text-blue-200">Overall Grade</div>
                    </div>
                    <div class="bg-gradient-to-br from-green-600 to-green-800 rounded-lg p-6 text-center">
                        <div class="text-3xl font-bold text-white">{"82" if is_subscriber else "78"}%</div>
                        <div class="text-green-200">Avg Success Rate</div>
                    </div>
                    <div class="bg-gradient-to-br from-purple-600 to-purple-800 rounded-lg p-6 text-center">
                        <div class="text-3xl font-bold text-white">{video_count if is_subscriber else "142"}</div>
                        <div class="text-purple-200">Videos Analyzed</div>
                    </div>
                    <div class="bg-gradient-to-br from-orange-600 to-orange-800 rounded-lg p-6 text-center">
                        <div class="text-3xl font-bold text-white">+{"18" if is_subscriber else "15"}%</div>
                        <div class="text-orange-200">This Month</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <div class="text-center py-8 mt-8">
        <p class="text-gray-400 text-sm">BJJ AI Analyzer Pro | Track Every Technique, Master Your Game</p>
        <p class="text-gray-500 text-xs mt-2">
            📱 Install as app: Chrome menu → "Add to Home Screen" | 
            🔒 Your data is private and secure
        </p>
    </div>

    <!-- Service Worker for PWA -->
    <script>
        if ('serviceWorker' in navigator) {{
            navigator.serviceWorker.register('/service-worker.js');
        }}
    </script>

    <script>
        let currentAnalysis = null;
        const userPlan = '{user_plan}';
        const isSubscriber = {str(is_subscriber).lower()};
        const hasTimestamps = {str(has_timestamps).lower()};

        // Tab Management
        function showTab(tabName) {{
            document.querySelectorAll('.tab-content').forEach(tab => {{
                tab.classList.remove('active');
            }});
            
            document.querySelectorAll('.tab-button').forEach(btn => {{
                btn.classList.remove('active');
            }});
            
            document.getElementById(tabName + '-tab').classList.add('active');
            event.target.classList.add('active');
            
            if (tabName === 'submissions') {{
                setTimeout(initSubmissionCharts, 100);
            }} else if (tabName === 'sweeps') {{
                setTimeout(initSweepCharts, 100);
            }} else if (tabName === 'passes') {{
                setTimeout(initPassCharts, 100);
            }} else if (tabName === 'takedowns') {{
                setTimeout(initTakedownCharts, 100);
            }}
        }}

        // Access Code Functions
        function showAccessCode() {{
            document.getElementById('access-code-modal').classList.remove('hidden');
        }}

        function hideAccessCode() {{
            document.getElementById('access-code-modal').classList.add('hidden');
            document.getElementById('access-code-input').value = '';
        }}

        async function redeemAccessCode() {{
            const code = document.getElementById('access-code-input').value.trim();
            if (!code) {{
                alert('Please enter an access code');
                return;
            }}

            try {{
                const response = await fetch('/api/redeem-code', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ code: code }})
                }});

                const result = await response.json();
                
                if (result.success) {{
                    alert('Access code redeemed successfully! Refreshing page...');
                    location.reload();
                }} else {{
                    alert(result.message || 'Invalid access code');
                }}
            }} catch (error) {{
                alert('Error redeeming code: ' + error.message);
            }}
        }}

        // Pricing Functions
        function showPricing() {{
            document.getElementById('pricing-modal').classList.remove('hidden');
        }}

        function hidePricing() {{
            document.getElementById('pricing-modal').classList.add('hidden');
        }}

        async function subscribeToPlan(plan) {{
            if (plan === 'free') {{
                alert('You are already on the free plan!');
                return;
            }}

            // In a real app, integrate with Stripe or payment processor
            const confirmed = confirm(`Subscribe to ${{plan.toUpperCase()}} plan? This will redirect to payment processing.`);
            
            if (confirmed) {{
                try {{
                    const response = await fetch('/api/subscribe', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ plan: plan }})
                    }});

                    const result = await response.json();
                    
                    if (result.success) {{
                        alert('Subscription successful! Welcome to ' + plan.toUpperCase() + '!');
                        location.reload();
                    }} else {{
                        alert(result.message || 'Subscription failed');
                    }}
                }} catch (error) {{
                    alert('Subscription error: ' + error.message);
                }}
            }}
        }}

        // Video Analysis
        async function analyzeVideo() {{
            const fileInput = document.getElementById('videoFile');
            if (!fileInput.files[0]) {{
                alert('Please select a video file first!');
                return;
            }}

            document.getElementById('upload-section').classList.add('hidden');
            document.getElementById('progress-section').classList.remove('hidden');

            let progress = 0;
            const progressBar = document.getElementById('progress-bar');
            
            const progressInterval = setInterval(() => {{
                progress += Math.random() * 12;
                if (progress > 100) progress = 100;
                progressBar.style.width = progress + '%';
                
                if (progress >= 100) {{
                    clearInterval(progressInterval);
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
                currentAnalysis = results;
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
            document.getElementById('video-length').textContent = results.video_duration + 's';
            document.getElementById('techniques-per-min').textContent = results.techniques_per_minute;
            
            const submissionCount = results.detected_techniques.filter(t => t.category === 'submission').length;
            document.getElementById('submission-count').textContent = submissionCount;

            displayTechniques(results.detected_techniques);
            displayInsights(results.insights);
        }}

        function displayTechniques(techniques) {{
            const techniquesList = document.getElementById('techniques-list');
            techniquesList.innerHTML = '';

            techniques.forEach(technique => {{
                const categoryColors = {{
                    'submission': 'border-l-red-500 bg-red-900',
                    'sweep': 'border-l-blue-500 bg-blue-900',
                    'guard_pass': 'border-l-green-500 bg-green-900',
                    'takedown': 'border-l-yellow-500 bg-yellow-900'
                }};

                const qualityColors = {{
                    'excellent': 'text-green-400',
                    'good': 'text-yellow-400',
                    'fair': 'text-orange-400'
                }};

                const categoryColor = categoryColors[technique.category] || 'border-l-gray-500 bg-gray-900';
                const qualityColor = qualityColors[technique.quality] || 'text-gray-400';

                const techniqueDiv = document.createElement('div');
                techniqueDiv.className = `${{categoryColor}} bg-opacity-30 border-l-4 rounded-lg p-4`;
                
                let timestampHTML = '';
                if (hasTimestamps && technique.video_timestamp) {{
                    timestampHTML = `
                        <button onclick="jumpToTimestamp(${{technique.start_time}})" 
                                class="video-timestamp bg-blue-600 hover:bg-blue-700 text-white px-2 py-1 rounded text-xs ml-2">
                            🎬 View in Video
                        </button>
                    `;
                }}

                techniqueDiv.innerHTML = `
                    <div class="flex justify-between items-center">
                        <div class="flex-1">
                            <div class="flex items-center space-x-2 mb-1">
                                <h4 class="text-lg font-bold text-white">${{formatTechniqueName(technique.technique)}}</h4>
                                <span class="px-2 py-1 bg-white bg-opacity-20 rounded text-xs text-gray-300">
                                    ${{technique.category.replace('_', ' ').toUpperCase()}}
                                </span>
                                ${{timestampHTML}}
                            </div>
                            <p class="text-gray-300 text-sm">
                                Time: ${{formatTime(technique.start_time)}} - ${{formatTime(technique.end_time)}} | 
                                Position: ${{technique.position}}
                            </p>
                        </div>
                        <div class="text-right">
                            <div class="text-white font-bold text-lg">${{Math.round(technique.confidence * 100)}}%</div>
                            <div class="text-sm ${{qualityColor}} font-semibold">${{technique.quality.toUpperCase()}}</div>
                        </div>
                    </div>
                `;
                
                techniquesList.appendChild(techniqueDiv);
            }});
        }}

        function jumpToTimestamp(seconds) {{
            alert(`Video timestamp feature: Jump to ${{formatTime(seconds)}}\\n\\nIn the full app, this would seek your video to the exact moment this technique was detected!`);
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

        // Chart Functions (simplified for demo)
        function initSubmissionCharts() {{
            const ctx = document.getElementById('submission-success-chart');
            if (!ctx || ctx.chart) return;

            const data = isSubscriber ? 
                [87, 72, 95, 65, 81] : // Real user data
                [87, 72, 95, 65, 81];  // Demo data

            ctx.chart = new Chart(ctx, {{
                type: 'doughnut',
                data: {{
                    labels: ['Armbar', 'Triangle', 'RNC', 'Kimura', 'Heel Hook'],
                    datasets: [{{
                        data: data,
                        backgroundColor: ['#ef4444', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6']
                    }}]
                }},
                options: {{
                    responsive: true,
                    plugins: {{
                        legend: {{ labels: {{ color: 'white' }} }}
                    }}
                }}
            }});
        }}

        function initSweepCharts() {{
            const ctx = document.getElementById('sweep-success-chart');
            if (!ctx || ctx.chart) return;

            ctx.chart = new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: ['Tripod', 'Scissor', 'Butterfly', 'Flower', 'DLR'],
                    datasets: [{{
                        label: 'Success Rate %',
                        data: [92, 68, 81, 55, 73],
                        backgroundColor: '#3b82f6'
                    }}]
                }},
                options: {{
                    responsive: true,
                    scales: {{
                        y: {{ ticks: {{ color: 'white' }} }},
                        x: {{ ticks: {{ color: 'white' }} }}
                    }},
                    plugins: {{
                        legend: {{ labels: {{ color: 'white' }} }}
                    }}
                }}
            }});
        }}

        function initPassCharts() {{
            const ctx = document.getElementById('pass-success-chart');
            if (!ctx || ctx.chart) return;

            ctx.chart = new Chart(ctx, {{
                type: 'polarArea',
                data: {{
                    labels: ['Knee Cut', 'Toreando', 'Leg Drag', 'Over Under', 'Stack'],
                    datasets: [{{
                        data: [82, 75, 88, 71, 60],
                        backgroundColor: ['#ef4444', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6']
                    }}]
                }},
                options: {{
                    responsive: true,
                    plugins: {{
                        legend: {{ labels: {{ color: 'white' }} }}
                    }},
                    scales: {{
                        r: {{ ticks: {{ color: 'white' }} }}
                    }}
                }}
            }});
        }}

        function initTakedownCharts() {{
            const ctx = document.getElementById('takedown-success-chart');
            if (!ctx || ctx.chart) return;

            ctx.chart = new Chart(ctx, {{
                type: 'radar',
                data: {{
                    labels: ['Double Leg', 'Single Leg', 'Hip Toss', 'Foot Sweep', 'Guard Pull'],
                    datasets: [{{
                        label: 'Success Rate',
                        data: [70, 55, 45, 38, 85],
                        borderColor: '#3b82f6',
                        backgroundColor: 'rgba(59, 130, 246, 0.2)'
                    }}]
                }},
                options: {{
                    responsive: true,
                    plugins: {{
                        legend: {{ labels: {{ color: 'white' }} }}
                    }},
                    scales: {{
                        r: {{ 
                            ticks: {{ color: 'white' }},
                            pointLabels: {{ color: 'white' }}
                        }}
                    }}
                }}
            }});
        }}

        // Utility Functions
        function formatTechniqueName(name) {{
            return name.replace(/_/g, ' ')
                      .split(' ')
                      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                      .join(' ');
        }}

        function formatTime(seconds) {{
            const mins = Math.floor(seconds / 60);
            const secs = Math.floor(seconds % 60);
            return `${{mins}}:${{secs.toString().padStart(2, '0')}}`;
        }}

        function resetApp() {{
            document.getElementById('upload-section').classList.remove('hidden');
            document.getElementById('progress-section').classList.add('hidden');
            document.getElementById('results-section').classList.add('hidden');
            document.getElementById('videoFile').value = '';
            currentAnalysis = null;
        }}

        // Initialize charts on load
        document.addEventListener('DOMContentLoaded', function() {{
            setTimeout(initSubmissionCharts, 500);
        }});
    </script>
</body>
</html>'''

@app.route('/api/redeem-code', methods=['POST'])
def redeem_access_code():
    user_id = get_user_id()
    data = request.get_json()
    code = data.get('code', '').strip().upper()
    
    plan = subscription_manager.validate_access_code(code)
    if plan:
        users_db[user_id]['plan'] = plan
        return jsonify({'success': True, 'message': f'Access code redeemed! You now have {plan} access.'})
    else:
        return jsonify({'success': False, 'message': 'Invalid or expired access code'})

@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    user_id = get_user_id()
    data = request.get_json()
    plan = data.get('plan')
    
    # In production, integrate with Stripe/payment processor here
    success = subscription_manager.subscribe_user(user_id, plan)
    
    if success:
        return jsonify({'success': True, 'message': f'Successfully subscribed to {plan} plan!'})
    else:
        return jsonify({'success': False, 'message': 'Subscription failed'})

@app.route('/api/analyze', methods=['POST'])
def analyze():
    user_id = get_user_id()
    user_plan = subscription_manager.get_user_plan(user_id)
    is_subscriber = subscription_manager.is_subscriber(user_id)
    has_timestamps = subscription_manager.has_video_timestamps(user_id)
    
    can_upload, message = subscription_manager.can_upload_video(user_id)
    if not can_upload:
        return jsonify({'error': message}), 403
    
    video_file = request.files.get('video')
    
    if is_subscriber:
        # Real analysis for subscribers
        result = analyzer.analyze_video_real(user_id, video_file, has_timestamps)
    else:
        # Demo analysis for non-subscribers
        result = analyzer.analyze_video_demo()
    
    return jsonify(result)

# PWA Manifest
@app.route('/manifest.json')
def manifest():
    return jsonify({
        "name": "BJJ AI Analyzer Pro",
        "short_name": "BJJ AI",
        "description": "Complete BJJ Analytics Platform",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#667eea",
        "theme_color": "#667eea",
        "orientation": "portrait",
        "icons": [
            {
                "src": "/static/icon-192.png",
                "sizes": "192x192",
                "type": "image/png"
            },
            {
                "src": "/static/icon-512.png", 
                "sizes": "512x512",
                "type": "image/png"
            }
        ]
    })

# Service Worker for PWA
@app.route('/service-worker.js')
def service_worker():
    return '''
self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open('bjj-ai-v1').then(function(cache) {
            return cache.addAll([
                '/',
                '/manifest.json',
                'https://cdn.tailwindcss.com',
                'https://cdn.jsdelivr.net/npm/chart.js'
            ]);
        })
    );
});

self.addEventListener('fetch', function(event) {
    event.respondWith(
        caches.match(event.request).then(function(response) {
            return response || fetch(event.request);
        })
    );
});
''', {'Content-Type': 'application/javascript'}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
            
            {f'''
            <div class="inline-block bg-green-600 text-white px-4 py-2 rounded-lg">
                Current Plan: {subscription_manager.plans[user_plan]["name"]} - ${subscription_manager.plans[user_plan]["price"]}/month
            </div>
            ''' if is_subscriber else '''
            <div class="space-x-4">
                <button onclick="showAccessCode()" class="bg-yellow-600 hover:bg-yellow-700 text-white px-4 py-2 rounded-lg font-bold">
                    📝 Have Access Code?
                </button>
                <button onclick="showPricing()" class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-bold">
                    🚀 SUBSCRIBE NOW
                </button>
            </div>
            '''}
        </div>
    </div>

    <!-- Access Code Modal -->
    <div id="access-code-modal" class="fixed inset-0 bg-black bg-opacity-50 hidden z-50 flex items-center justify-center">
        <div class="glass rounded-xl p-8 max-w-md mx-4">
            <div class="text-center">
                <h2 class="text-2xl font-bold text-white mb-4">Enter Access Code</h2>
                <input type="text" id="access-code-input" placeholder="Enter your access code" 
                       class="w-full p-3 rounded-lg bg-white bg-opacity-20 text-white placeholder-gray-300 mb-4">
                <div class="space-x-4">
                    <button onclick="redeemAccessCode()" class="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg font-bold">
                        Redeem Code
                    </button>
                    <button onclick="hideAccessCode()" class="bg-gray-600 hover:bg-gray-700 text-white px-6 py-2 rounded-lg">
                        Cancel
                    </button>
                </div>
                <p class="text-gray-300 text-sm mt-4">Try: BJJ2024FREE, GUARD2024, SWEEP2024</p>
            </div>
        </div>
    </div>

    <!-- Pricing Modal -->
    <div id="pricing-modal" class="fixed inset-0 bg-black bg-opacity-50 hidden z-50 flex items-center justify-center">
        <div class="glass rounded-xl p-8 max-w-5xl mx-4 max-h-screen overflow-y-auto">
            <div class="flex justify-between items-center mb-6">
                <h2 class="text-2xl font-bold text-white">Choose Your Plan</h2>
                <button onclick="hidePricing()" class="text-white text-2xl">&times;</button>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <!-- Free Plan -->
                <div class="bg-white bg-opacity-10 rounded-lg p-6 text-center relative">
                    <h3 class="text-xl font-bold text-white mb-2">Free Monthly</h3>
                    <div class="text-3xl font-bold text-gray-300 mb-4">$0<span class="text-sm">/month</span></div>
                    <ul class="text-gray-300 space-y-2 mb-6 text-sm">
                        <li>• 1 video analysis per month</li>
                        <li>• Basic technique detection</li>
                        <li>• Demo analytics view</li>
                        <li>• Limited insights</li>
                    </ul>
                    <button onclick="subscribeToPlan('free')" class="bg-gray-600 text-white py-2 px-4 rounded-lg font-bold w-full">
                        Current Plan
                    </button>
                </div>
                
                <!-- Pro Plan -->
                <div class="bg-blue-600 bg-opacity-20 rounded-lg p-6 text-center border-2 border-blue-400 relative">
                    <div class="bg-blue-500 text-white px-3 py-1 rounded-full text-xs absolute -top-3 left-1/2 transform -translate-x-1/2">
                        MOST POPULAR
                    </div>
                    <h3 class="text-xl font-bold text-white mb-2">BJJ Pro</h3>
                    <div class="text-3xl font-bold text-white mb-4">$20<span class="text-sm">/month</span></div>
                    <ul class="text-white space-y-2 mb-6 text-sm">
                        <li>• Unlimited video analysis</li>
                        <li>• Real personal analytics</li>
                        <li>• Progress tracking</li>
                        <li>• Training recommendations</li>
                        <li>• Success rate tracking</li>
                        <li>• Export reports</li>
                    </ul>
                    <button onclick="subscribeToPlan('pro')" class="bg-blue-600 hover:bg-blue-700 text-white py-2 px-6 rounded-lg font-bold w-full">
                        Subscribe Now
                    </button>
                </div>
                
                <!-- Elite Plan -->
                <div class="bg-purple-600 bg-opacity-20 rounded-lg p-6 text-center border-2 border-purple-400 relative">
                    <div class="bg-purple-500 text-white px-3 py-1 rounded-full text-xs absolute -top-3 left-1/2 transform -translate-x-1/2">
                        ELITE FEATURES
                    </div>
                    <h3 class="text-xl font-bold text-white mb-2">Elite Competitor</h3>
                    <div class="text-3xl font-bold text-white mb-4">$50<span class="text-sm">/month</span></div>
                    <ul class="text-white space-y-2 mb-6 text-sm">
                        <li>• Everything in Pro</li>
                        <li>• 📽️ Video timestamp linking</li>
                        <li>• Frame-by-frame analysis</li>
                        <li>• Competition tools</li>
                        <li>• Opponent scouting</li>
                        <li>• Advanced biomechanics</li>
                        <li>• Priority support</li>
                        <li>• Beta features</li>
                    </ul>
                    <button onclick="subscribeToPlan('elite')" class="bg-purple-600 hover:bg-purple-700 text-white py-2 px-6 rounded-lg font-bold w-full">
                        Subscribe Now
                    </button>
                </div>
            </div>
            
            <div class="mt-8 text-center">
                <p class="text-gray-300 text-sm">💳 Secure payment processing • Cancel anytime • 30-day money-back guarantee</p>
            </div>
        </div>
    </div>

    <!-- Navigation Tabs -->
    <div class="container mx-auto px-4 max-w-6xl mb-8">
        <div class="glass rounded-xl p-2">
            <div class="flex flex-wrap justify-center space-x-1 md:space-x-2">
                <button onclick="showTab('upload')" class="tab-button active px-3 md:px-6 py-2 rounded-lg text-white font-semibold text-sm md:text-base">
                    📹 Upload
                </button>
                <button onclick="showTab('submissions')" class="tab-button px-3 md:px-6 py-2 rounded-lg text-white font-semibold text-sm md:text-base relative">
                    🎯 Submissions
                    {'' if is_subscriber else '<span class="demo-badge">DEMO</span>'}
                </button>
                <button onclick="showTab('sweeps')" class="tab-button px-3 md:px-6 py-2 rounded-lg text-white font-semibold text-sm md:text-base relative">
                    🌊 Sweeps
                    {'' if is_subscriber else '<span class="demo-badge">DEMO</span>'}
                </button>
                <button onclick="showTab('passes')" class="tab-button px-3 md:px-6 py-2 rounded-lg text-white font-semibold text-sm md:text-base relative">
                    🛡️ Passes
                    {'' if is_subscriber else '<span class="demo-badge">DEMO</span>'}
                </button>
                <button onclick="showTab('takedowns')" class="tab-button px-3 md:px-6 py-2 rounded-lg text-white font-semibold text-sm md:text-base relative">
                    🤼 Takedowns
                    {'' if is_subscriber else '<span class="demo-badge">DEMO</span>'}
                </button>
                <button onclick="showTab('analytics')" class="tab-button px-3 md:px-6 py-2 rounded-lg text-white font-semibold text-sm md:text-base relative">
                    📊 Analytics
                    {'' if is_subscriber else '<span class="demo-badge">DEMO</span>'}
                </button>
            </div>
        </div>
    </div>

    <div class="container mx-auto px-4 max-w-6xl">
        <!-- Upload Tab -->
        <div id="upload-tab" class="tab-content active">
            <div id="upload-section" class="glass rounded-xl p-8 mb-8">
                <h2 class="text-2xl font-bold text-white mb-6 text-center">Upload Your BJJ Video</h2>
                
                {"" if can_upload else f'''
                <div class="bg-red-900 bg-opacity-50 rounded-lg p-6 text-center mb-6">
                    <h3 class="text-xl font-bold text-white mb-2">🚫 Upload Not Available</h3>
                    <p class="text-gray-300 mb-4">{upload_message}</p>
                    <div class="space-x-4">
                        <button onclick="showAccessCode()" class="bg-yellow-600 hover:bg-yellow-700 text-white font-bold py-2 px-4 rounded-lg">
                            Use Access Code
                        </button>
                        <button onclick="showPricing()" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg">
                            Subscribe Now
                        </button>
                    </div>
                </div>
                '''}
                
                {f'''
                <div class="text-center">
                    <input type="file" id="videoFile" accept="video/*" class="mb-4 text-white">
                    <br>
                    {f'<p class="text-green-300 text-sm mb-4">✅ {user_plan.title()} Plan - Real analysis will be performed</p>' if is_subscriber else '<p class="text-yellow-300 text-sm mb-4">👀 Demo user - Sample analysis will be shown</p>'}
                    <button onclick="analyzeVideo()" id="analyzeBtn" 
                            class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-lg">
                        🤖 Analyze Techniques
                    </button>
                    {f'<p class="text-purple-300 text-xs mt-2">🎬 Elite plan: Video timestamps included!</p>' if has_timestamps else ''}
                </div>
                ''' if can_upload else ''}
            </div>
