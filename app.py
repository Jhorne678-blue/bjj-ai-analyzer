from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime
import time

app = Flask(__name__)

class SimpleBJJAnalyzer:
    def analyze_video(self, video_name):
        time.sleep(3)  # Pretend to think for 3 seconds
        
        return {
            'total_techniques_detected': 3,
            'detected_techniques': [
                {'technique': 'armbar_from_guard', 'confidence': 0.87, 'start_time': 15, 'end_time': 25, 'quality': 'good'},
                {'technique': 'tripod_sweep', 'confidence': 0.92, 'start_time': 45, 'end_time': 55, 'quality': 'excellent'},
                {'technique': 'guard_position', 'confidence': 0.78, 'start_time': 10, 'end_time': 60, 'quality': 'good'}
            ],
            'video_duration': 120,
            'techniques_per_minute': 1.5,
            'average_confidence': 0.86
        }

analyzer = SimpleBJJAnalyzer()

@app.route('/')
def home():
    return '''<!DOCTYPE html>
<html>
<head>
    <title>BJJ AI Analyzer</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .glass { background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); }
    </style>
</head>
<body class="min-h-screen">
    <div class="text-center py-8">
        <h1 class="text-5xl font-bold text-white mb-4">🥋 BJJ AI Analyzer</h1>
        <p class="text-xl text-gray-200">Free AI-Powered BJJ Technique Analysis</p>
    </div>

    <div class="container mx-auto px-4 max-w-4xl">
        <div id="upload-section" class="glass rounded-xl p-8">
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

        <div id="results" class="glass rounded-xl p-8 mt-8 hidden">
            <h3 class="text-2xl font-bold text-white mb-6">📊 Analysis Results</h3>
            <div id="techniques-list"></div>
            <button onclick="resetApp()" class="bg-green-600 text-white font-bold py-2 px-6 rounded-lg mt-4">
                📹 Analyze Another Video
            </button>
        </div>
    </div>

    <script>
        function analyzeVideo() {
            const fileInput = document.getElementById('videoFile');
            if (!fileInput.files[0]) {
                alert('Please select a video file first!');
                return;
            }

            document.getElementById('upload-section').classList.add('hidden');
            document.getElementById('results').classList.remove('hidden');
            
            document.getElementById('techniques-list').innerHTML = '<p class="text-white">Analyzing... 🤖</p>';

            fetch('/api/analyze', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    let html = '<div class="space-y-4">';
                    data.detected_techniques.forEach(tech => {
                        html += `<div class="bg-white bg-opacity-20 rounded-lg p-4">
                            <h4 class="text-white font-bold">${tech.technique.replace(/_/g, ' ').toUpperCase()}</h4>
                            <p class="text-gray-300">Confidence: ${Math.round(tech.confidence * 100)}% | Quality: ${tech.quality}</p>
                        </div>`;
                    });
                    html += '</div>';
                    document.getElementById('techniques-list').innerHTML = html;
                });
        }

        function resetApp() {
            document.getElementById('upload-section').classList.remove('hidden');
            document.getElementById('results').classList.add('hidden');
            document.getElementById('videoFile').value = '';
        }
    </script>
</body>
</html>'''

@app.route('/api/analyze', methods=['POST'])
def analyze():
    result = analyzer.analyze_video("demo_video.mp4")
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
