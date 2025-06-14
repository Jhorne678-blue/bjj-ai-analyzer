from flask import Flask, render_template, request, jsonify, session
import os
import time
import json
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = 'bjj-secret-2024'

# Simple user storage
users = {}
subscriptions = {}

@app.route('/')
def home():
    return '''<!DOCTYPE html>
<html>
<head>
    <title>BJJ AI Analyzer Pro</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }</style>
</head>
<body class="min-h-screen">
    <div class="text-center py-8">
        <h1 class="text-5xl font-bold text-white mb-4">🥋 BJJ AI Analyzer Pro</h1>
        <p class="text-xl text-gray-200">Complete BJJ Analytics Platform</p>
        
        <div class="mt-8 space-y-4">
            <div class="bg-white bg-opacity-20 rounded-lg p-6 max-w-2xl mx-auto">
                <h2 class="text-2xl font-bold text-white mb-4">Choose Your Plan</h2>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div class="bg-white bg-opacity-10 rounded-lg p-4">
                        <h3 class="text-lg font-bold text-white">Free Monthly</h3>
                        <div class="text-2xl font-bold text-white">$0</div>
                        <p class="text-gray-300">1 video per month</p>
                    </div>
                    
                    <div class="bg-blue-600 bg-opacity-30 rounded-lg p-4 border-2 border-blue-400">
                        <h3 class="text-lg font-bold text-white">BJJ Pro</h3>
                        <div class="text-2xl font-bold text-white">$20</div>
                        <p class="text-gray-300">Unlimited videos</p>
                    </div>
                    
                    <div class="bg-purple-600 bg-opacity-30 rounded-lg p-4">
                        <h3 class="text-lg font-bold text-white">Elite</h3>
                        <div class="text-2xl font-bold text-white">$50</div>
                        <p class="text-gray-300">Video timestamps</p>
                    </div>
                </div>
                
                <div class="mt-6">
                    <input type="text" id="accessCode" placeholder="Enter access code (try: BJJ2024FREE)" 
                           class="p-3 rounded-lg w-64 mr-4">
                    <button onclick="redeemCode()" class="bg-green-600 text-white px-6 py-3 rounded-lg font-bold">
                        Redeem Code
                    </button>
                </div>
                
                <div class="mt-6">
                    <input type="file" id="videoFile" accept="video/*" class="mb-4">
                    <br>
                    <button onclick="analyzeVideo()" class="bg-blue-600 text-white px-8 py-3 rounded-lg font-bold">
                        🤖 Analyze Video
                    </button>
                </div>
                
                <div id="results" class="mt-6 hidden">
                    <h3 class="text-xl font-bold text-white">Analysis Results</h3>
                    <div class="bg-white bg-opacity-10 rounded p-4 mt-4">
                        <p class="text-white">✅ Armbar from Guard detected at 0:15 (87% confidence)</p>
                        <p class="text-white">✅ Tripod Sweep detected at 1:23 (92% confidence)</p>
                        <p class="text-white">✅ Triangle Choke detected at 2:45 (78% confidence)</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        function redeemCode() {
            const code = document.getElementById('accessCode').value;
            if (code === 'BJJ2024FREE' || code === 'GUARD2024' || code === 'SWEEP2024') {
                alert('✅ Access code redeemed! You now have free access!');
            } else {
                alert('❌ Invalid access code. Try: BJJ2024FREE');
            }
        }
        
        function analyzeVideo() {
            const file = document.getElementById('videoFile').files[0];
            if (!file) {
                alert('Please select a video file first!');
                return;
            }
            
            alert('🤖 Analyzing video... (This is a demo version)');
            document.getElementById('results').classList.remove('hidden');
        }
    </script>
</body>
</html>'''

@app.route('/api/test')
def test():
    return jsonify({'status': 'working', 'message': 'BJJ AI is running!'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
