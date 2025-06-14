from flask import Flask, render_template, request, jsonify
import os
import json
from datetime import datetime, timedelta
import time
import random

app = Flask(__name__)

class CompleteBJJAnalyzer:
    def __init__(self):
        # Complete BJJ technique database
        self.bjj_techniques = {
            'submissions': {
                'gi': [
                    'collar_choke', 'bow_and_arrow', 'loop_choke', 'ezekiel_choke', 'baseball_choke',
                    'clock_choke', 'paper_cutter_choke', 'bow_and_arrow_choke', 'lapel_choke'
                ],
                'nogi': [
                    'rear_naked_choke', 'darce_choke', 'anaconda_choke', 'arm_triangle', 
                    'north_south_choke', 'guillotine_choke', 'peruvian_necktie'
                ],
                'joint_locks': [
                    'armbar_from_guard', 'armbar_from_mount', 'triangle_choke', 'kimura', 
                    'americana', 'omoplata', 'gogoplata', 'heel_hook', 'ankle_lock', 
                    'toe_hold', 'knee_bar', 'calf_slicer', 'bicep_slicer'
                ]
            },
            'sweeps': {
                'closed_guard': ['scissor_sweep', 'flower_sweep', 'hip_bump_sweep'],
                'open_guard': ['tripod_sweep', 'tomoe_nage', 'butterfly_sweep'],
                'spider_guard': ['spider_guard_sweep', 'lasso_sweep'],
                'de_la_riva': ['de_la_riva_sweep', 'berimbolo'],
                'x_guard': ['x_guard_sweep', 'single_leg_x_sweep'],
                'other': ['elevator_sweep', 'pendulum_sweep', 'sit_up_sweep']
            },
            'guard_passes': [
                'knee_cut_pass', 'toreando_pass', 'stack_pass', 'leg_drag_pass', 
                'over_under_pass', 'double_under_pass', 'x_pass', 'headquarters_pass',
                'knee_shield_pass', 'smash_pass', 'pressure_pass'
            ],
            'takedowns': {
                'wrestling': ['double_leg_takedown', 'single_leg_takedown', 'high_crotch', 'ankle_pick'],
                'judo': ['hip_toss', 'foot_sweep', 'osoto_gari', 'ouchi_gari', 'seoi_nage'],
                'other': ['guard_pull', 'flying_armbar', 'flying_triangle']
            },
            'positions': [
                'closed_guard', 'open_guard', 'half_guard', 'side_control', 'mount', 
                'back_control', 'knee_on_belly', 'north_south', 'turtle', 'standing'
            ],
            'escapes': [
                'mount_escape', 'side_control_escape', 'back_escape', 'guard_retention',
                'turtle_escape', 'knee_on_belly_escape'
            ]
        }
        
        # Sample athlete data for analytics
        self.sample_athlete_data = {
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
            },
            'most_vulnerable_to': {
                'submissions': {'heel_hook': 67, 'triangle_choke': 45, 'rear_naked_choke': 32},
                'sweeps': {'de_la_riva_sweep': 55, 'butterfly_sweep': 43, 'scissor_sweep': 38},
                'passes': {'knee_cut_pass': 48, 'toreando_pass': 35, 'leg_drag_pass': 41},
                'takedowns': {'foot_sweep': 52, 'double_leg_takedown': 28, 'hip_toss': 19}
            }
        }

    def analyze_video(self, video_name):
        # Simulate analysis time
        time.sleep(3)
        
        # Generate realistic random techniques
        detected_techniques = []
        
        # Add submissions
        submission_techniques = ['armbar_from_guard', 'triangle_choke', 'rear_naked_choke', 'kimura', 'heel_hook']
        for i, tech in enumerate(random.sample(submission_techniques, 3)):
            detected_techniques.append({
                'technique': tech,
                'category': 'submission',
                'confidence': round(random.uniform(0.75, 0.98), 2),
                'start_time': 20 + i * 25,
                'end_time': 30 + i * 25,
                'quality': random.choice(['excellent', 'good', 'fair']),
                'position': random.choice(['guard', 'mount', 'side_control', 'back_control'])
            })
        
        # Add sweeps
        sweep_techniques = ['tripod_sweep', 'scissor_sweep', 'butterfly_sweep', 'flower_sweep']
        for i, tech in enumerate(random.sample(sweep_techniques, 2)):
            detected_techniques.append({
                'technique': tech,
                'category': 'sweep',
                'confidence': round(random.uniform(0.70, 0.95), 2),
                'start_time': 100 + i * 20,
                'end_time': 110 + i * 20,
                'quality': random.choice(['excellent', 'good', 'fair']),
                'position': 'guard'
            })
        
        # Add guard passes
        pass_techniques = ['knee_cut_pass', 'toreando_pass', 'leg_drag_pass']
        for i, tech in enumerate(random.sample(pass_techniques, 2)):
            detected_techniques.append({
                'technique': tech,
                'category': 'guard_pass',
                'confidence': round(random.uniform(0.65, 0.90), 2),
                'start_time': 160 + i * 15,
                'end_time': 170 + i * 15,
                'quality': random.choice(['excellent', 'good', 'fair']),
                'position': 'guard'
            })
        
        # Add takedowns
        takedown_techniques = ['double_leg_takedown', 'single_leg_takedown', 'hip_toss']
        tech = random.choice(takedown_techniques)
        detected_techniques.append({
            'technique': tech,
            'category': 'takedown',
            'confidence': round(random.uniform(0.70, 0.88), 2),
            'start_time': 5,
            'end_time': 12,
            'quality': random.choice(['excellent', 'good']),
            'position': 'standing'
        })
        
        # Calculate analytics
        total_techniques = len(detected_techniques)
        avg_confidence = sum(t['confidence'] for t in detected_techniques) / total_techniques
        
        # Generate insights
        insights = self.generate_insights(detected_techniques)
        
        return {
            'total_techniques_detected': total_techniques,
            'detected_techniques': detected_techniques,
            'video_duration': 240,
            'techniques_per_minute': round(total_techniques / 4, 1),
            'average_confidence': round(avg_confidence, 2),
            'analysis_timestamp': datetime.now().isoformat(),
            'category_breakdown': self.get_category_breakdown(detected_techniques),
            'insights': insights,
            'athlete_stats': self.sample_athlete_data
        }
    
    def get_category_breakdown(self, techniques):
        breakdown = {}
        for tech in techniques:
            category = tech['category']
            if category not in breakdown:
                breakdown[category] = 0
            breakdown[category] += 1
        return breakdown
    
    def generate_insights(self, techniques):
        insights = []
        
        # Analyze technique quality
        excellent_count = sum(1 for t in techniques if t['quality'] == 'excellent')
        if excellent_count >= 3:
            insights.append("🔥 Excellent technique execution! You're showing high-level skills.")
        
        # Analyze submission attempts
        submissions = [t for t in techniques if t['category'] == 'submission']
        if len(submissions) >= 3:
            insights.append("🎯 High submission rate detected. You're actively hunting for finishes!")
        
        # Analyze guard play
        guard_techniques = [t for t in techniques if t['position'] == 'guard']
        if len(guard_techniques) >= 4:
            insights.append("🛡️ Strong guard game! You're comfortable working from bottom position.")
        
        # Analyze confidence scores
        high_confidence = [t for t in techniques if t['confidence'] > 0.85]
        if len(high_confidence) >= 4:
            insights.append("📈 High detection confidence suggests clean, textbook technique execution.")
        
        return insights

analyzer = CompleteBJJAnalyzer()

@app.route('/')
def home():
    return '''<!DOCTYPE html>
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
        .pulse { animation: pulse 2s infinite; }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
    </style>
</head>
<body class="min-h-screen">
    <!-- Header -->
    <div class="text-center py-8">
        <h1 class="text-5xl font-bold text-white mb-4">🥋 BJJ AI Analyzer Pro</h1>
        <p class="text-xl text-gray-200">Complete BJJ Analytics Platform</p>
        <p class="text-sm text-gray-300 mt-2">Upload, Analyze, Improve - Track Every Technique</p>
    </div>

    <!-- Navigation Tabs -->
    <div class="container mx-auto px-4 max-w-6xl mb-8">
        <div class="glass rounded-xl p-2">
            <div class="flex flex-wrap justify-center space-x-2">
                <button onclick="showTab('upload')" class="tab-button active px-6 py-2 rounded-lg text-white font-semibold transition-all">
                    📹 Upload & Analyze
                </button>
                <button onclick="showTab('submissions')" class="tab-button px-6 py-2 rounded-lg text-white font-semibold transition-all">
                    🎯 Submissions
                </button>
                <button onclick="showTab('sweeps')" class="tab-button px-6 py-2 rounded-lg text-white font-semibold transition-all">
                    🌊 Sweeps
                </button>
                <button onclick="showTab('passes')" class="tab-button px-6 py-2 rounded-lg text-white font-semibold transition-all">
                    🛡️ Guard Passes
                </button>
                <button onclick="showTab('takedowns')" class="tab-button px-6 py-2 rounded-lg text-white font-semibold transition-all">
                    🤼 Takedowns
                </button>
                <button onclick="showTab('analytics')" class="tab-button px-6 py-2 rounded-lg text-white font-semibold transition-all">
                    📊 Analytics
                </button>
            </div>
        </div>
    </div>

    <div class="container mx-auto px-4 max-w-6xl">
        <!-- Upload Tab -->
        <div id="upload-tab" class="tab-content active">
            <div id="upload-section" class="glass rounded-xl p-8 mb-8">
                <h2 class="text-2xl font-bold text-white mb-6 text-center">Upload Your BJJ Video</h2>
                <div class="text-center">
                    <input type="file" id="videoFile" accept="video/*" class="mb-4 text-white">
                    <br>
                    <button onclick="analyzeVideo()" id="analyzeBtn" 
                            class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-lg">
                        🤖 Analyze Techniques
                    </button>
                </div>
            </div>

            <div id="progress-section" class="glass rounded-xl p-6 mb-8 hidden">
                <h3 class="text-xl font-bold text-white mb-4">🔍 Analyzing Your Video...</h3>
                <div class="w-full bg-gray-700 rounded-full h-4 mb-4">
                    <div id="progress-bar" class="bg-blue-600 h-4 rounded-full transition-all duration-500" style="width: 0%"></div>
                </div>
                <p class="text-gray-300 text-center"><span class="pulse">🧠</span> AI is detecting BJJ techniques...</p>
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
                        <div class="text-gray-300 text-sm">Video Length</div>
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
            <div class="glass rounded-xl p-8">
                <h2 class="text-2xl font-bold text-white mb-6">🎯 Submission Analytics</h2>
                
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    <!-- Your Success Rates -->
                    <div class="bg-white bg-opacity-10 rounded-lg p-6">
                        <h3 class="text-xl font-bold text-white mb-4">Your Success Rates</h3>
                        <canvas id="submission-success-chart" width="400" height="300"></canvas>
                    </div>
                    
                    <!-- Most Vulnerable To -->
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
                            <div class="flex justify-between items-center">
                                <span class="text-gray-300">RNC</span>
                                <div class="flex items-center">
                                    <div class="w-24 h-3 bg-gray-700 rounded-full mr-2">
                                        <div class="h-3 bg-green-500 rounded-full" style="width: 32%"></div>
                                    </div>
                                    <span class="text-green-400 font-bold">32%</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Recommendations -->
                <div class="mt-8 bg-blue-900 bg-opacity-50 rounded-lg p-6">
                    <h3 class="text-xl font-bold text-white mb-4">🎯 Training Recommendations</h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="bg-white bg-opacity-10 rounded p-4">
                            <h4 class="font-bold text-white mb-2">Focus Areas</h4>
                            <ul class="text-gray-300 space-y-1">
                                <li>• Heel hook defense (3x/week)</li>
                                <li>• Triangle escape fundamentals</li>
                                <li>• Leg entanglement awareness</li>
                            </ul>
                        </div>
                        <div class="bg-white bg-opacity-10 rounded p-4">
                            <h4 class="font-bold text-white mb-2">Strengths to Develop</h4>
                            <ul class="text-gray-300 space-y-1">
                                <li>• RNC setups from back control</li>
                                <li>• Armbar variations from guard</li>
                                <li>• Triangle finishing details</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Sweeps Tab -->
        <div id="sweeps-tab" class="tab-content">
            <div class="glass rounded-xl p-8">
                <h2 class="text-2xl font-bold text-white mb-6">🌊 Sweep Analytics</h2>
                
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    <div class="bg-white bg-opacity-10 rounded-lg p-6">
                        <h3 class="text-xl font-bold text-white mb-4">Your Best Sweeps</h3>
                        <canvas id="sweep-success-chart" width="400" height="300"></canvas>
                    </div>
                    
                    <div class="bg-white bg-opacity-10 rounded-lg p-6">
                        <h3 class="text-xl font-bold text-white mb-4">Getting Swept By</h3>
                        <div class="space-y-4">
                            <div class="bg-white bg-opacity-10 rounded p-4">
                                <div class="flex justify-between items-center mb-2">
                                    <span class="font-bold text-white">De La Riva Sweep</span>
                                    <span class="text-red-400 font-bold">55%</span>
                                </div>
                                <p class="text-gray-300 text-sm">Work on DLR guard retention and hook defense</p>
                            </div>
                            <div class="bg-white bg-opacity-10 rounded p-4">
                                <div class="flex justify-between items-center mb-2">
                                    <span class="font-bold text-white">Butterfly Sweep</span>
                                    <span class="text-yellow-400 font-bold">43%</span>
                                </div>
                                <p class="text-gray-300 text-sm">Practice underhook prevention and base</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Guard Passes Tab -->
        <div id="passes-tab" class="tab-content">
            <div class="glass rounded-xl p-8">
                <h2 class="text-2xl font-bold text-white mb-6">🛡️ Guard Pass Analytics</h2>
                
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    <div class="bg-white bg-opacity-10 rounded-lg p-6">
                        <h3 class="text-xl font-bold text-white mb-4">Your Passing Success</h3>
                        <canvas id="pass-success-chart" width="400" height="300"></canvas>
                    </div>
                    
                    <div class="bg-white bg-opacity-10 rounded-lg p-6">
                        <h3 class="text-xl font-bold text-white mb-4">How You Get Passed</h3>
                        <div class="space-y-3">
                            <div class="flex justify-between items-center">
                                <span class="text-gray-300">Knee Cut Pass</span>
                                <span class="text-red-400 font-bold">48%</span>
                            </div>
                            <div class="flex justify-between items-center">
                                <span class="text-gray-300">Leg Drag Pass</span>
                                <span class="text-yellow-400 font-bold">41%</span>
                            </div>
                            <div class="flex justify-between items-center">
                                <span class="text-gray-300">Toreando Pass</span>
                                <span class="text-green-400 font-bold">35%</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Takedowns Tab -->
        <div id="takedowns-tab" class="tab-content">
            <div class="glass rounded-xl p-8">
                <h2 class="text-2xl font-bold text-white mb-6">🤼 Takedown Analytics</h2>
                
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    <div class="bg-white bg-opacity-10 rounded-lg p-6">
                        <h3 class="text-xl font-bold text-white mb-4">Your Takedown Success</h3>
                        <canvas id="takedown-success-chart" width="400" height="300"></canvas>
                    </div>
                    
                    <div class="bg-white bg-opacity-10 rounded-lg p-6">
                        <h3 class="text-xl font-bold text-white mb-4">Takedown Defense</h3>
                        <div class="space-y-4">
                            <div class="text-center mb-4">
                                <div class="text-3xl font-bold text-green-400">73%</div>
                                <div class="text-gray-300">Overall Defense Rate</div>
                            </div>
                            <div class="space-y-3">
                                <div class="flex justify-between">
                                    <span class="text-gray-300">vs Double Leg</span>
                                    <span class="text-green-400">82%</span>
                                </div>
                                <div class="flex justify-between">
                                    <span class="text-gray-300">vs Single Leg</span>
                                    <span class="text-yellow-400">67%</span>
                                </div>
                                <div class="flex justify-between">
                                    <span class="text-gray-300">vs Foot Sweeps</span>
                                    <span class="text-red-400">45%</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Analytics Tab -->
        <div id="analytics-tab" class="tab-content">
            <div class="glass rounded-xl p-8">
                <h2 class="text-2xl font-bold text-white mb-6">📊 Complete Analytics Dashboard</h2>
                
                <!-- Overall Performance -->
                <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                    <div class="bg-gradient-to-br from-blue-600 to-blue-800 rounded-lg p-6 text-center">
                        <div class="text-3xl font-bold text-white">B+</div>
                        <div class="text-blue-200">Overall Grade</div>
                    </div>
                    <div class="bg-gradient-to-br from-green-600 to-green-800 rounded-lg p-6 text-center">
                        <div class="text-3xl font-bold text-white">78%</div>
                        <div class="text-green-200">Avg Success Rate</div>
                    </div>
                    <div class="bg-gradient-to-br from-purple-600 to-purple-800 rounded-lg p-6 text-center">
                        <div class="text-3xl font-bold text-white">142</div>
                        <div class="text-purple-200">Videos Analyzed</div>
                    </div>
                    <div class="bg-gradient-to-br from-orange-600 to-orange-800 rounded-lg p-6 text-center">
                        <div class="text-3xl font-bold text-white">+15%</div>
                        <div class="text-orange-200">This Month</div>
                    </div>
                </div>

                <!-- Style Analysis -->
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
                    <div class="bg-white bg-opacity-10 rounded-lg p-6">
                        <h3 class="text-xl font-bold text-white mb-4">🎭 Your BJJ Style Profile</h3>
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
                                    <span class="text-gray-300">Pressure Passer</span>
                                    <span class="text-white">72%</span>
                                </div>
                                <div class="w-full bg-gray-700 rounded-full h-2">
                                    <div class="bg-green-500 h-2 rounded-full" style="width: 72%"></div>
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
                            <div>
                                <div class="flex justify-between mb-1">
                                    <span class="text-gray-300">Takedown Artist</span>
                                    <span class="text-white">45%</span>
                                </div>
                                <div class="w-full bg-gray-700 rounded-full h-2">
                                    <div class="bg-yellow-500 h-2 rounded-full" style="width: 45%"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="bg-white bg-opacity-10 rounded-lg p-6">
                        <h3 class="text-xl font-bold text-white mb-4">📈 Progress Over Time</h3>
                        <canvas id="progress-chart" width="400" height="200"></canvas>
                    </div>
                </div>

                <!-- Recommendations -->
                <div class="bg-white bg-opacity-10 rounded-lg p-6">
                    <h3 class="text-xl font-bold text-white mb-4">🎯 Personalized Training Plan</h3>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <div class="bg-red-900 bg-opacity-50 rounded-lg p-4">
                            <h4 class="font-bold text-white mb-2">🚨 Priority Areas</h4>
                            <ul class="text-gray-300 space-y-1 text-sm">
                                <li>• Heel hook defense (Critical)</li>
                                <li>• Foot sweep defense</li>
                                <li>• DLR guard retention</li>
                            </ul>
                        </div>
                        <div class="bg-yellow-900 bg-opacity-50 rounded-lg p-4">
                            <h4 class="font-bold text-white mb-2">⚡ Skills to Develop</h4>
                            <ul class="text-gray-300 space-y-1 text-sm">
                                <li>• Takedown entries</li>
                                <li>• Leg drag passing</li>
                                <li>• Triangle finishing</li>
                            </ul>
                        </div>
                        <div class="bg-green-900 bg-opacity-50 rounded-lg p-4">
                            <h4 class="font-bold text-white mb-2">💪 Strengths to Exploit</h4>
                            <ul class="text-gray-300 space-y-1 text-sm">
                                <li>• Submission hunting</li>
                                <li>• Guard retention</li>
                                <li>• RNC from back control</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <div class="text-center py-8 mt-8">
        <p class="text-gray-400 text-sm">BJJ AI Analyzer Pro | Track Every Technique, Master Your Game</p>
    </div>

    <script>
        let currentAnalysis = null;

        // Tab Management
        function showTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Remove active from all buttons
            document.querySelectorAll('.tab-button').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Show selected tab
            document.getElementById(tabName + '-tab').classList.add('active');
            
            // Activate button
            event.target.classList.add('active');
            
            // Initialize charts when tabs are shown
            if (tabName === 'submissions') {
                setTimeout(initSubmissionCharts, 100);
            } else if (tabName === 'sweeps') {
                setTimeout(initSweepCharts, 100);
            } else if (tabName === 'passes') {
                setTimeout(initPassCharts, 100);
            } else if (tabName === 'takedowns') {
                setTimeout(initTakedownCharts, 100);
            } else if (tabName === 'analytics') {
                setTimeout(initAnalyticsCharts, 100);
            }
        }

        // Video Analysis
        function analyzeVideo() {
            const fileInput = document.getElementById('videoFile');
            if (!fileInput.files[0]) {
                alert('Please select a video file first!');
                return;
            }

            document.getElementById('upload-section').classList.add('hidden');
            document.getElementById('progress-section').classList.remove('hidden');

            let progress = 0;
            const progressBar = document.getElementById('progress-bar');
            
            const progressInterval = setInterval(() => {
                progress += Math.random() * 15;
                if (progress > 100) progress = 100;
                progressBar.style.width = progress + '%';
                
                if (progress >= 100) {
                    clearInterval(progressInterval);
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
                currentAnalysis = results;
                displayResults(results);
            } catch (error) {
                alert('Analysis failed: ' + error.message);
                resetApp();
            }
        }

        function displayResults(results) {
            document.getElementById('progress-section').classList.add('hidden');
            document.getElementById('results-section').classList.remove('hidden');

            // Update stats
            document.getElementById('total-count').textContent = results.total_techniques_detected;
            document.getElementById('avg-confidence').textContent = Math.round(results.average_confidence * 100) + '%';
            document.getElementById('video-length').textContent = results.video_duration + 's';
            document.getElementById('techniques-per-min').textContent = results.techniques_per_minute;
            
            const submissionCount = results.detected_techniques.filter(t => t.category === 'submission').length;
            document.getElementById('submission-count').textContent = submissionCount;

            // Display techniques
            displayTechniques(results.detected_techniques);
            
            // Display insights
            displayInsights(results.insights);
        }

        function displayTechniques(techniques) {
            const techniquesList = document.getElementById('techniques-list');
            techniquesList.innerHTML = '';

            if (techniques.length === 0) {
                techniquesList.innerHTML = '<p class="text-gray-300 text-center">No techniques detected.</p>';
                return;
            }

            techniques.forEach((technique, index) => {
                const categoryColors = {
                    'submission': 'border-l-red-500 bg-red-900',
                    'sweep': 'border-l-blue-500 bg-blue-900',
                    'guard_pass': 'border-l-green-500 bg-green-900',
                    'takedown': 'border-l-yellow-500 bg-yellow-900'
                };

                const qualityColors = {
                    'excellent': 'text-green-400',
                    'good': 'text-yellow-400',
                    'fair': 'text-orange-400'
                };

                const categoryColor = categoryColors[technique.category] || 'border-l-gray-500 bg-gray-900';
                const qualityColor = qualityColors[technique.quality] || 'text-gray-400';

                const techniqueDiv = document.createElement('div');
                techniqueDiv.className = `${categoryColor} bg-opacity-30 border-l-4 rounded-lg p-4 flex justify-between items-center`;
                techniqueDiv.innerHTML = `
                    <div class="flex-1">
                        <div class="flex items-center space-x-2 mb-1">
                            <h4 class="text-lg font-bold text-white">${formatTechniqueName(technique.technique)}</h4>
                            <span class="px-2 py-1 bg-white bg-opacity-20 rounded text-xs text-gray-300">${technique.category.replace('_', ' ').toUpperCase()}</span>
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
                `;
                techniquesList.appendChild(techniqueDiv);
            });
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

        // Chart Initialization Functions
        function initSubmissionCharts() {
            const ctx = document.getElementById('submission-success-chart');
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

        function initSweepCharts() {
            const ctx = document.getElementById('sweep-success-chart');
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

        function initPassCharts() {
            const ctx = document.getElementById('pass-success-chart');
            if (!ctx || ctx.chart) return;

            ctx.chart = new Chart(ctx, {
                type: 'polarArea',
                data: {
                    labels: ['Knee Cut', 'Toreando', 'Leg Drag', 'Over Under', 'Stack'],
                    datasets: [{
                        data: [82, 75, 88, 71, 60],
                        backgroundColor: ['#ef4444', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6']
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

        function initTakedownCharts() {
            const ctx = document.getElementById('takedown-success-chart');
            if (!ctx || ctx.chart) return;

            ctx.chart = new Chart(ctx, {
                type: 'radar',
                data: {
                    labels: ['Double Leg', 'Single Leg', 'Hip Toss', 'Foot Sweep', 'Guard Pull'],
                    datasets: [{
                        label: 'Success Rate',
                        data: [70, 55, 45, 38, 85],
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

        function initAnalyticsCharts() {
            const ctx = document.getElementById('progress-chart');
            if (!ctx || ctx.chart) return;

            ctx.chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                    datasets: [{
                        label: 'Overall Performance',
                        data: [65, 68, 72, 75, 78, 82],
                        borderColor: '#10b981',
                        backgroundColor: 'rgba(16, 185, 129, 0.1)',
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { labels: { color: 'white' } }
                    },
                    scales: {
                        y: { 
                            ticks: { color: 'white' },
                            min: 50,
                            max: 100
                        },
                        x: { ticks: { color: 'white' } }
                    }
                }
            });
        }

        // Utility Functions
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
            document.getElementById('upload-section').classList.remove('hidden');
            document.getElementById('progress-section').classList.add('hidden');
            document.getElementById('results-section').classList.add('hidden');
            document.getElementById('videoFile').value = '';
            currentAnalysis = null;
        }

        // Initialize default charts on page load
        document.addEventListener('DOMContentLoaded', function() {
            // Small delay to ensure DOM is ready
            setTimeout(initSubmissionCharts, 500);
        });
    </script>
</body>
</html>'''

@app.route('/api/analyze', methods=['POST'])
def analyze():
    result = analyzer.analyze_video("demo_video.mp4")
    return jsonify(result)

@app.route('/api/stats')
def get_stats():
    return jsonify(analyzer.sample_athlete_data)

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
