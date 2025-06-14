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
                        
                        <div class="mt-6">
                            <h4 class="text-lg font-bold text-white mb-3">🎯 Training Recommendations</h4>
                            <div class="space-y-2">
                                <div class="bg-red-900 bg-opacity-50 rounded p-3">
                                    <p class="text-red-300 font-bold text-sm">Priority: Heel Hook Defense</p>
                                    <p class="text-gray-300 text-xs">Practice leg entanglement awareness daily</p>
                                </div>
                                <div class="bg-yellow-900 bg-opacity-50 rounded p-3">
                                    <p class="text-yellow-300 font-bold text-sm">Improve: Triangle Escapes</p>
                                    <p class="text-gray-300 text-xs">Work on posture and hand positioning</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="mt-8">
                    <h3 class="text-xl font-bold text-white mb-4">📈 Submission Breakdown by Position</h3>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div class="bg-white bg-opacity-10 rounded-lg p-4">
                            <h4 class="font-bold text-white mb-2">From Guard</h4>
                            <div class="space-y-1 text-sm">
                                <div class="flex justify-between">
                                    <span class="text-gray-300">Armbar</span>
                                    <span class="text-blue-400">87%</span>
                                </div>
                                <div class="flex justify-between">
                                    <span class="text-gray-300">Triangle</span>
                                    <span class="text-green-400">72%</span>
                                </div>
                                <div class="flex justify-between">
                                    <span class="text-gray-300">Omoplata</span>
                                    <span class="text-yellow-400">52%</span>
                                </div>
                            </div>
                        </div>
                        <div class="bg-white bg-opacity-10 rounded-lg p-4">
                            <h4 class="font-bold text-white mb-2">From Back Control</h4>
                            <div class="space-y-1 text-sm">
                                <div class="flex justify-between">
                                    <span class="text-gray-300">RNC</span>
                                    <span class="text-green-400">95%</span>
                                </div>
                                <div class="flex justify-between">
                                    <span class="text-gray-300">Collar Choke</span>
                                    <span class="text-blue-400">78%</span>
                                </div>
                            </div>
                        </div>
                        <div class="bg-white bg-opacity-10 rounded-lg p-4">
                            <h4 class="font-bold text-white mb-2">From Side Control</h4>
                            <div class="space-y-1 text-sm">
                                <div class="flex justify-between">
                                    <span class="text-gray-300">Kimura</span>
                                    <span class="text-yellow-400">65%</span>
                                </div>
                                <div class="flex justify-between">
                                    <span class="text-gray-300">Americana</span>
                                    <span class="text-orange-400">58%</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Sweeps Tab -->
        <div id="sweeps-tab" class="tab-content">
            <div class="glass rounded-xl p-8 relative">
                {'' if user_plan != "demo" else '<div class="demo-badge">DEMO DATA</div>'}
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
                            <div class="bg-white bg-opacity-10 rounded p-4">
                                <div class="flex justify-between items-center mb-2">
                                    <span class="font-bold text-white">Scissor Sweep</span>
                                    <span class="text-green-400 font-bold">38%</span>
                                </div>
                                <p class="text-gray-300 text-sm">Good defense - maintain low posture</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="mt-8">
                    <h3 class="text-xl font-bold text-white mb-4">🎯 Sweep Success by Guard Type</h3>
                    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                        <div class="bg-gradient-to-br from-blue-600 to-blue-800 rounded-lg p-4 text-center">
                            <div class="text-2xl font-bold text-white">84%</div>
                            <div class="text-blue-200 text-sm">Closed Guard</div>
                        </div>
                        <div class="bg-gradient-to-br from-green-600 to-green-800 rounded-lg p-4 text-center">
                            <div class="text-2xl font-bold text-white">76%</div>
                            <div class="text-green-200 text-sm">Open Guard</div>
                        </div>
                        <div class="bg-gradient-to-br from-purple-600 to-purple-800 rounded-lg p-4 text-center">
                            <div class="text-2xl font-bold text-white">69%</div>
                            <div class="text-purple-200 text-sm">Half Guard</div>
                        </div>
                        <div class="bg-gradient-to-br from-orange-600 to-orange-800 rounded-lg p-4 text-center">
                            <div class="text-2xl font-bold text-white">91%</div>
                            <div class="text-orange-200 text-sm">Butterfly</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Guard Passes Tab -->
        <div id="passes-tab" class="tab-content">
            <div class="glass rounded-xl p-8 relative">
                {'' if user_plan != "demo" else '<div class="demo-badge">DEMO DATA</div>'}
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
                        
                        <div class="mt-6">
                            <h4 class="text-lg font-bold text-white mb-3">📊 Guard Retention Rate</h4>
                            <div class="text-center mb-4">
                                <div class="text-4xl font-bold text-blue-400">67%</div>
                                <div class="text-gray-300">Overall Retention</div>
                            </div>
                            <div class="space-y-2">
                                <div class="flex justify-between">
                                    <span class="text-gray-300 text-sm">vs Pressure Passing</span>
                                    <span class="text-red-400 text-sm">52%</span>
                                </div>
                                <div class="flex justify-between">
                                    <span class="text-gray-300 text-sm">vs Speed Passing</span>
                                    <span class="text-green-400 text-sm">78%</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Takedowns Tab -->
        <div id="takedowns-tab" class="tab-content">
            <div class="glass rounded-xl p-8 relative">
                {'' if user_plan != "demo" else '<div class="demo-badge">DEMO DATA</div>'}
                <h2 class="text-2xl font-bold text-white mb-6">🤼 Takedown Analytics</h2>
                
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    <div class="bg-white bg-opacity-10 rounded-lg p-6">
                        <h3 class="text-xl font-bold text-white mb-4">Your Takedown Success</h3>
                        <canvas id="takedown-success-chart" width="400" height="300"></canvas>
                    </div>
                    
                    <div class="bg-white bg-opacity-10 rounded-lg p-6">
                        <h3 class="text-xl font-bold text-white mb-4">Takedown Defense</h3>
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
                            <div class="flex justify-between">
                                <span class="text-gray-300">vs Hip Throws</span>
                                <span class="text-blue-400">71%</span>
                            </div>
                        </div>
                        
                        <div class="mt-6">
                            <h4 class="text-lg font-bold text-white mb-3">🎯 Focus Areas</h4>
                            <div class="bg-red-900 bg-opacity-50 rounded p-3">
                                <p class="text-red-300 font-bold text-sm">Weak Against: Foot Sweeps</p>
                                <p class="text-gray-300 text-xs">Practice balance and stance awareness</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Analytics Tab -->
        <div id="analytics-tab" class="tab-content">
            <div class="glass rounded-xl p-8 relative">
                {'' if user_plan != "demo" else '<div class="demo-badge">DEMO DATA</div>'}
                <h2 class="text-2xl font-bold text-white mb-6">📊 Complete Analytics Dashboard</h2>
                
                <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                    <div class="bg-gradient-to-br from-blue-600 to-blue-800 rounded-lg p-6 text-center">
                        <div class="text-3xl font-bold text-white">{"A-" if user_plan != "demo" else "B+"}</div>
                        <div class="text-blue-200">Overall Grade</div>
                    </div>
                    <div class="bg-gradient-to-br from-green-600 to-green-800 rounded-lg p-6 text-center">
                        <div class="text-3xl font-bold text-white">{"82" if user_plan != "demo" else "78"}%</div>
                        <div class="text-green-200">Avg Success Rate</div>
                    </div>
                    <div class="bg-gradient-to-br from-purple-600 to-purple-800 rounded-lg p-6 text-center">
                        <div class="text-3xl font-bold text-white">{user_videos_count if user_plan != "demo" else "142"}</div>
                        <div class="text-purple-200">Videos Analyzed</div>
                    </div>
                    <div class="bg-gradient-to-br from-orange-600 to-orange-800 rounded-lg p-6 text-center">
                        <div class="text-3xl font-bold text-white">+{"18" if user_plan != "demo" else "15"}%</div>
                        <div class="text-orange-200">This Month</div>
                    </div>
                </div>

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

                <div class="bg-white bg-opacity-10 rounded-lg p-6">
                    <h3 class="text-xl font-bold text-white mb-4">🎯 Personalized Training Plan</h3>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <div class="bg-red-900 bg-opacity-50 rounded-lg p-4">
                            <h4 class="font-bold text-white mb-2">🚨 Priority Areas</h4>
                            <ul class="text-gray-300 space-y-1 text-sm">
                                <li>• Heel hook defense (Critical)</li>
                                <li>• Foot sweep defense</li>
                                <li>• DLR guard retention</li>
                                <li>• Triangle escape timing</li>
                            </ul>
                        </div>
                        <div class="bg-yellow-900 bg-opacity-50 rounded-lg p-4">
                            <h4 class="font-bold text-white mb-2">⚡ Skills to Develop</h4>
                            <ul class="text-gray-300 space-y-1 text-sm">
                                <li>• Takedown entries</li>
                                <li>• Leg drag passing</li>
                                <li>• Triangle finishing</li>
                                <li>• Pressure passing</li>
                            </ul>
                        </div>
                        <div class="bg-green-900 bg-opacity-50 rounded-lg p-4">
                            <h4 class="font-bold text-white mb-2">💪 Strengths to Exploit</h4>
                            <ul class="text-gray-300 space-y-1 text-sm">
                                <li>• Submission hunting</li>
                                <li>• Guard retention</li>
                                <li>• RNC from back control</li>
                                <li>• Butterfly sweeps</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="text-center py-8 mt-8">
        <p class="text-gray-400 text-sm">BJJ AI Analyzer Pro | Track Every Technique, Master Your Game</p>
    </div>

    <script>
        let currentAnalysis = null;
        const userPlan = '{user_plan}';

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
            }} else if (tabName === 'analytics') {{
                setTimeout(initAnalyticsCharts, 100);
            }}
        }}

        // Modal functions
        function showAccessCode() {{
            document.getElementById('access-code-modal').classList.remove('hidden');
        }}

        function hideAccessCode() {{
            document.getElementById('access-code-modal').classList.add('hidden');
            document.getElementById('access-code-input').value = '';
        }}

        function showPricing() {{
            document.getElementById('pricing-modal').classList.remove('hidden');
        }}

        function hidePricing() {{
            document.getElementById('pricing-modal').classList.add('hidden');
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
                    alert('✅ Access code redeemed successfully! Refreshing page...');
                    location.reload();
                }} else {{
                    alert('❌ ' + (result.message || 'Invalid access code'));
                }}
            }} catch (error) {{
                alert('Error redeeming code: ' + error.message);
            }}
        }}

        function subscribeToPlan(plan) {{
            alert(`🚀 Subscribing to ${{plan.toUpperCase()}} plan!\\n\\nThis would redirect to payment processing.\\n\\nFor demo, use access code "BJJ2024FREE"`);
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
                    'takedown': 'border-l-yellow-500 bg-yellow-900',
                    'position': 'border-l-purple-500 bg-purple-900',
                    'escape': 'border-l-orange-500 bg-orange-900'
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
                if (technique.video_timestamp && technique.video_timestamp.clickable) {{
                    timestampHTML = `
                        <button onclick="jumpToTimestamp(${{technique.start_time}})" 
                                class="bg-blue-600 hover:bg-blue-700 text-white px-2 py-1 rounded text-xs ml-2">
                            🎬 Jump to ${{formatTime(technique.start_time)}}
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
                                Position: ${{technique.position}} | Setup: ${{technique.setup_type}}
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
            alert(`🎬 Elite Feature: Jump to ${{formatTime(seconds)}}\\n\\nIn the full app, this would seek your video to the exact moment!`);
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

        // Chart Functions
        function initSubmissionCharts() {{
            const ctx = document.getElementById('submission-success-chart');
            if (!ctx || ctx.chart) return;

            ctx.chart = new Chart(ctx, {{
                type: 'doughnut',
                data: {{
                    labels: ['Armbar', 'Triangle', 'RNC', 'Kimura', 'Heel Hook', 'Ankle Lock'],
                    datasets: [{{
                        data: [87, 72, 95, 65, 81, 73],
                        backgroundColor: ['#ef4444', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#06b6d4']
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
                    labels: ['Tripod', 'Scissor', 'Butterfly', 'Flower', 'DLR', 'X-Guard'],
                    datasets: [{{
                        label: 'Success Rate %',
                        data: [92, 68, 81, 55, 73, 78],
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
                    labels: ['Knee Cut', 'Toreando', 'Leg Drag', 'Over Under', 'Stack', 'Smash'],
                    datasets: [{{
                        data: [82, 75, 88, 71, 60, 77],
                        backgroundColor: ['#ef4444', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#06b6d4']
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
                    labels: ['Double Leg', 'Single Leg', 'Hip Toss', 'Foot Sweep', 'Guard Pull', 'High Crotch'],
                    datasets: [{{
                        label: 'Success Rate',
                        data: [70, 55, 45, 38, 85, 63],
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

        function initAnalyticsCharts() {{
            const ctx = document.getElementById('progress-chart');
            if (!ctx || ctx.chart) return;

            ctx.chart = new Chart(ctx, {{
                type: 'line',
                data: {{
                    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                    datasets: [{{
                        label: 'Overall Performance',
                        data: [65, 68, 72, 75, 78, 82],
                        borderColor: '#10b981',
                        backgroundColor: 'rgba(16, 185, 129, 0.1)',
                        tension: 0.4
                    }}]
                }},
                options: {{
                    responsive: true,
                    plugins: {{
                        legend: {{ labels: {{ color: 'white' }} }}
                    }},
                    scales: {{
                        y: {{ 
                            ticks: {{ color: 'white' }},
                            min: 50,
                            max: 100
                        }},
                        x: {{ ticks: {{ color: 'white' }} }}
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

        // Initialize default charts on page load
        document.addEventListener('DOMContentLoaded', function() {{
            setTimeout(initSubmissionCharts, 500);
        }});
    </script>
</body>
</html>'''

@app.route('/api/redeem-code', methods=['POST'])
def redeem_code():
    user_id = get_user_id()
    data = request.get_json()
    code = data.get('code', '').upper()
    
    if code in access_codes and access_codes[code]['uses'] > 0:
        access_codes[code]['uses'] -= 1
        users[user_id]['plan'] = access_codes[code]['plan']
        return jsonify({'success': True, 'message': f'Access code redeemed! You now have {access_codes[code]["plan"]} access.'})
    else:
        return jsonify({'success': False, 'message': 'Invalid or expired access code'})

@app.route('/api/analyze', methods=['POST'])
def analyze():
    user_id = get_user_id()
    user_plan = users[user_id]['plan']
    
    if user_plan == 'demo':
        return jsonify({'error': 'Please use access code or subscribe first'}), 403
    
    # Check monthly limit for free users
    if user_plan == 'free':
        current_month = datetime.now().strftime('%Y-%m')
        monthly_videos = [v for v in user_videos.get(user_id, []) if v.get('timestamp', '').startswith(current_month)]
        if len(monthly_videos) >= 1:
            return jsonify({'error': 'Free plan limit reached (1 video per month). Upgrade to Pro for unlimited!'}), 403
    
    # Simulate AI processing time
    time.sleep(4)
    
    # Generate comprehensive analysis
    include_timestamps = (user_plan == 'elite')
    analysis_result = generate_realistic_analysis(user_plan, include_timestamps)
    
    # Store the analysis for the user
    analysis_result['id'] = f"analysis_{len(user_videos.get(user_id, []))}"
    analysis_result['timestamp'] = datetime.now().isoformat()
    
    if user_id not in user_videos:
        user_videos[user_id] = []
    user_videos[user_id].append(analysis_result)
    
    # Update user stats
    users[user_id]['total_videos'] += 1
    
    return jsonify(analysis_result)

@app.route('/api/stats')
def get_user_stats():
    user_id = get_user_id()
    user_plan = users[user_id]['plan']
    
    if user_plan == 'demo':
        return jsonify(DEMO_STATS)
    
    # Calculate real stats from user's videos
    videos = user_videos.get(user_id, [])
    if not videos:
        return jsonify({'message': 'Upload more videos to see personalized statistics!'})
    
    # Aggregate user's real data
    all_techniques = []
    for video in videos:
        all_techniques.extend(video.get('detected_techniques', []))
    
    # Calculate success rates by category
    real_stats = {'total_videos': len(videos), 'total_techniques': len(all_techniques)}
    
    for category in ['submission', 'sweep', 'guard_pass', 'takedown']:
        category_techniques = [t for t in all_techniques if t['category'] == category]
        if category_techniques:
            avg_confidence = sum(t['confidence'] for t in category_techniques) / len(category_techniques)
            real_stats[f'{category}_avg_confidence'] = round(avg_confidence * 100)
    
    return jsonify(real_stats)

@app.route('/api/status')
def status():
    return jsonify({
        'status': 'running',
        'message': 'BJJ AI Analyzer Pro is online!',
        'version': '2.0',
        'features': ['Complete Analytics', 'Subscription System', 'Video Timestamps']
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)from flask import Flask, request, jsonify, session
import os
import json
import time
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'bjj-ai-secret-2024'

# Complete storage
users = {}
user_videos = {}
access_codes = {
    'BJJ2024FREE': {'plan': 'free', 'uses': 100},
    'GUARD2024': {'plan': 'free', 'uses': 100},
    'SWEEP2024': {'plan': 'free', 'uses': 100},
    'SUBMIT2024': {'plan': 'free', 'uses': 100},
    'ESCAPE2024': {'plan': 'free', 'uses': 100}
}

# Complete BJJ technique database
TECHNIQUES_DB = {
    'submissions': {
        'gi': ['collar_choke', 'bow_and_arrow', 'loop_choke', 'ezekiel_choke', 'baseball_choke'],
        'nogi': ['rear_naked_choke', 'darce_choke', 'anaconda_choke', 'arm_triangle', 'guillotine_choke'],
        'joint_locks': ['armbar_from_guard', 'armbar_from_mount', 'triangle_choke', 'kimura', 'americana', 'omoplata', 'heel_hook', 'ankle_lock', 'knee_bar']
    },
    'sweeps': {
        'closed_guard': ['scissor_sweep', 'flower_sweep', 'hip_bump_sweep'],
        'open_guard': ['tripod_sweep', 'tomoe_nage', 'butterfly_sweep'],
        'spider_guard': ['spider_guard_sweep', 'lasso_sweep'],
        'de_la_riva': ['de_la_riva_sweep', 'berimbolo'],
        'x_guard': ['x_guard_sweep', 'single_leg_x_sweep']
    },
    'guard_passes': ['knee_cut_pass', 'toreando_pass', 'stack_pass', 'leg_drag_pass', 'over_under_pass', 'double_under_pass', 'smash_pass'],
    'takedowns': {
        'wrestling': ['double_leg_takedown', 'single_leg_takedown', 'high_crotch', 'ankle_pick'],
        'judo': ['hip_toss', 'foot_sweep', 'osoto_gari', 'ouchi_gari', 'seoi_nage']
    },
    'positions': ['closed_guard', 'open_guard', 'half_guard', 'side_control', 'mount', 'back_control', 'knee_on_belly'],
    'escapes': ['mount_escape', 'side_control_escape', 'back_escape', 'guard_retention']
}

# Demo analytics data
DEMO_STATS = {
    'submission_success_rates': {
        'armbar_from_guard': 87, 'triangle_choke': 72, 'rear_naked_choke': 95,
        'kimura': 65, 'americana': 58, 'heel_hook': 81, 'ankle_lock': 73,
        'darce_choke': 69, 'guillotine_choke': 76, 'omoplata': 52
    },
    'sweep_success_rates': {
        'tripod_sweep': 92, 'scissor_sweep': 68, 'butterfly_sweep': 81,
        'flower_sweep': 55, 'de_la_riva_sweep': 73, 'x_guard_sweep': 78,
        'hip_bump_sweep': 61, 'spider_guard_sweep': 84
    },
    'guard_pass_success_rates': {
        'knee_cut_pass': 82, 'toreando_pass': 75, 'stack_pass': 60,
        'leg_drag_pass': 88, 'over_under_pass': 71, 'smash_pass': 77
    },
    'takedown_success_rates': {
        'double_leg_takedown': 70, 'single_leg_takedown': 55, 'hip_toss': 45,
        'foot_sweep': 38, 'guard_pull': 85, 'high_crotch': 63
    },
    'vulnerable_to': {
        'submissions': {'heel_hook': 67, 'triangle_choke': 45, 'rear_naked_choke': 32},
        'sweeps': {'de_la_riva_sweep': 55, 'butterfly_sweep': 43, 'scissor_sweep': 38},
        'passes': {'knee_cut_pass': 48, 'toreando_pass': 35, 'leg_drag_pass': 41},
        'takedowns': {'foot_sweep': 52, 'double_leg_takedown': 28}
    }
}

def get_user_id():
    if 'user_id' not in session:
        session['user_id'] = f"user_{random.randint(1000, 9999)}"
        users[session['user_id']] = {
            'plan': 'demo',
            'videos_this_month': 0,
            'created_at': datetime.now().isoformat(),
            'total_videos': 0
        }
        user_videos[session['user_id']] = []
    return session['user_id']

def generate_realistic_analysis(user_plan, include_timestamps=False):
    """Generate comprehensive BJJ analysis"""
    
    # Generate 8-15 techniques across all categories
    all_techniques = []
    technique_categories = ['submission', 'sweep', 'guard_pass', 'takedown', 'position', 'escape']
    
    num_techniques = random.randint(8, 15)
    
    for i in range(num_techniques):
        category = random.choice(technique_categories)
        
        # Select technique based on category
        if category == 'submission':
            techniques_list = ['armbar_from_guard', 'triangle_choke', 'rear_naked_choke', 'kimura', 'americana', 'heel_hook', 'ankle_lock', 'darce_choke', 'guillotine_choke', 'omoplata']
        elif category == 'sweep':
            techniques_list = ['tripod_sweep', 'scissor_sweep', 'butterfly_sweep', 'flower_sweep', 'de_la_riva_sweep', 'x_guard_sweep', 'hip_bump_sweep']
        elif category == 'guard_pass':
            techniques_list = ['knee_cut_pass', 'toreando_pass', 'stack_pass', 'leg_drag_pass', 'over_under_pass', 'smash_pass']
        elif category == 'takedown':
            techniques_list = ['double_leg_takedown', 'single_leg_takedown', 'hip_toss', 'foot_sweep', 'guard_pull', 'high_crotch']
        elif category == 'position':
            techniques_list = ['closed_guard', 'open_guard', 'mount', 'side_control', 'back_control', 'half_guard']
        else:  # escape
            techniques_list = ['mount_escape', 'side_control_escape', 'back_escape', 'guard_retention']
        
        technique = random.choice(techniques_list)
        start_time = random.randint(10, 280)
        end_time = start_time + random.randint(8, 25)
        confidence = round(random.uniform(0.65, 0.98), 2)
        
        technique_data = {
            'technique': technique,
            'category': category,
            'confidence': confidence,
            'start_time': start_time,
            'end_time': end_time,
            'quality': 'excellent' if confidence > 0.85 else 'good' if confidence > 0.75 else 'fair',
            'position': random.choice(['guard', 'mount', 'side_control', 'standing', 'back_control', 'half_guard']),
            'setup_type': random.choice(['chain', 'single', 'counter', 'transition']),
            'opponent_reaction': random.choice(['defended', 'completed', 'escaped', 'countered'])
        }
        
        # Add video timestamps for Elite users
        if include_timestamps:
            technique_data['video_timestamp'] = {
                'start_url': f"#t={start_time}",
                'end_url': f"#t={end_time}",
                'clickable': True
            }
        
        all_techniques.append(technique_data)
    
    # Calculate comprehensive stats
    total_techniques = len(all_techniques)
    avg_confidence = sum(t['confidence'] for t in all_techniques) / total_techniques
    video_duration = random.randint(180, 420)
    
    # Category breakdown
    category_counts = {}
    for tech in all_techniques:
        cat = tech['category']
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    # Quality breakdown
    quality_counts = {'excellent': 0, 'good': 0, 'fair': 0}
    for tech in all_techniques:
        quality_counts[tech['quality']] += 1
    
    # Generate insights
    insights = []
    
    # Technique diversity
    if len(set(t['category'] for t in all_techniques)) >= 5:
        insights.append("🎯 Excellent technique diversity! You're showing a well-rounded BJJ game across multiple categories.")
    
    # Quality analysis
    if quality_counts['excellent'] >= 4:
        insights.append("🔥 Outstanding execution quality! Multiple techniques performed at an excellent level.")
    
    # Category-specific insights
    submissions = [t for t in all_techniques if t['category'] == 'submission']
    if len(submissions) >= 4:
        insights.append("🎯 Submission-focused rolling! You're actively hunting for finishes and showing killer instinct.")
    
    sweeps = [t for t in all_techniques if t['category'] == 'sweep']
    if len(sweeps) >= 3:
        insights.append("🌊 Strong sweep game detected! You're effective at off-balancing and reversing position.")
    
    guard_passes = [t for t in all_techniques if t['category'] == 'guard_pass']
    if len(guard_passes) >= 3:
        insights.append("🛡️ Solid guard passing skills! You're methodical in breaking down guard systems.")
    
    # Position analysis
    guard_work = [t for t in all_techniques if t['position'] == 'guard']
    if len(guard_work) >= 5:
        insights.append("🛡️ Guard specialist detected! You're comfortable working from bottom position.")
    
    # Setup analysis
    chain_attacks = [t for t in all_techniques if t['setup_type'] == 'chain']
    if len(chain_attacks) >= 3:
        insights.append("⛓️ Great chain attacks! You're linking techniques together effectively.")
    
    # Success rate analysis
    completed_techniques = [t for t in all_techniques if t['opponent_reaction'] == 'completed']
    if len(completed_techniques) >= 5:
        insights.append("✅ High success rate! You're finishing your techniques effectively.")
    
    return {
        'total_techniques_detected': total_techniques,
        'detected_techniques': all_techniques,
        'video_duration': video_duration,
        'techniques_per_minute': round(total_techniques / (video_duration / 60), 1),
        'average_confidence': round(avg_confidence, 2),
        'category_breakdown': category_counts,
        'quality_breakdown': quality_counts,
        'insights': insights,
        'analysis_timestamp': datetime.now().isoformat(),
        'user_plan': user_plan,
        'has_timestamps': include_timestamps
    }

@app.route('/')
def home():
    user_id = get_user_id()
    user_plan = users[user_id]['plan']
    user_videos_count = len(user_videos.get(user_id, []))
    
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
        .demo-badge {{ position: absolute; top: 10px; right: 10px; background: rgba(255, 193, 7, 0.9); color: black; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }}
        .pulse {{ animation: pulse 2s infinite; }}
        @keyframes pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.5; }} }}
    </style>
</head>
<body class="min-h-screen">
    <!-- Header -->
    <div class="text-center py-8">
        <h1 class="text-5xl font-bold text-white mb-4">🥋 BJJ AI Analyzer Pro</h1>
        <p class="text-xl text-gray-200">Complete BJJ Analytics Platform</p>
        
        <div class="mt-4 space-y-2">
            <div class="flex justify-center items-center space-x-4">
                {"✅" if user_plan != "demo" else "👀"} 
                <span class="text-lg font-bold text-white">
                    {user_plan.upper()} {"MEMBER" if user_plan != "demo" else "DEMO"}
                </span>
                {f"• {user_videos_count} Videos Analyzed" if user_videos_count > 0 else ""}
            </div>
            
            {f'''
            <div class="inline-block bg-green-600 text-white px-4 py-2 rounded-lg">
                Current Plan: {user_plan.title()} Plan
            </div>
            ''' if user_plan != "demo" else '''
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
                <div class="bg-white bg-opacity-10 rounded-lg p-6 text-center">
                    <h3 class="text-xl font-bold text-white mb-2">Free Monthly</h3>
                    <div class="text-3xl font-bold text-gray-300 mb-4">$0<span class="text-sm">/month</span></div>
                    <ul class="text-gray-300 space-y-2 mb-6 text-sm">
                        <li>• 1 video analysis per month</li>
                        <li>• Basic technique detection</li>
                        <li>• Demo analytics view</li>
                        <li>• Limited insights</li>
                    </ul>
                    <button onclick="alert('Use access code to get free plan!')" class="bg-gray-600 text-white py-2 px-4 rounded-lg font-bold w-full">
                        Need Access Code
                    </button>
                </div>
                
                <div class="bg-blue-600 bg-opacity-20 rounded-lg p-6 text-center border-2 border-blue-400">
                    <div class="bg-blue-500 text-white px-3 py-1 rounded-full text-xs mb-2">MOST POPULAR</div>
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
                
                <div class="bg-purple-600 bg-opacity-20 rounded-lg p-6 text-center border-2 border-purple-400">
                    <div class="bg-purple-500 text-white px-3 py-1 rounded-full text-xs mb-2">ELITE FEATURES</div>
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
                    </ul>
                    <button onclick="subscribeToPlan('elite')" class="bg-purple-600 hover:bg-purple-700 text-white py-2 px-6 rounded-lg font-bold w-full">
                        Subscribe Now
                    </button>
                </div>
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
                    {'' if user_plan != "demo" else '<span class="demo-badge">DEMO</span>'}
                </button>
                <button onclick="showTab('sweeps')" class="tab-button px-3 md:px-6 py-2 rounded-lg text-white font-semibold text-sm md:text-base relative">
                    🌊 Sweeps
                    {'' if user_plan != "demo" else '<span class="demo-badge">DEMO</span>'}
                </button>
                <button onclick="showTab('passes')" class="tab-button px-3 md:px-6 py-2 rounded-lg text-white font-semibold text-sm md:text-base relative">
                    🛡️ Passes
                    {'' if user_plan != "demo" else '<span class="demo-badge">DEMO</span>'}
                </button>
                <button onclick="showTab('takedowns')" class="tab-button px-3 md:px-6 py-2 rounded-lg text-white font-semibold text-sm md:text-base relative">
                    🤼 Takedowns
                    {'' if user_plan != "demo" else '<span class="demo-badge">DEMO</span>'}
                </button>
                <button onclick="showTab('analytics')" class="tab-button px-3 md:px-6 py-2 rounded-lg text-white font-semibold text-sm md:text-base relative">
                    📊 Analytics
                    {'' if user_plan != "demo" else '<span class="demo-badge">DEMO</span>'}
                </button>
            </div>
        </div>
    </div>

    <div class="container mx-auto px-4 max-w-6xl">
        <!-- Upload Tab -->
        <div id="upload-tab" class="tab-content active">
            <div id="upload-section" class="glass rounded-xl p-8 mb-8">
                <h2 class="text-2xl font-bold text-white mb-6 text-center">Upload Your BJJ Video</h2>
                
                {"" if user_plan != "demo" else f'''
                <div class="bg-red-900 bg-opacity-50 rounded-lg p-6 text-center mb-6">
                    <h3 class="text-xl font-bold text-white mb-2">🚫 Upload Not Available</h3>
                    <p class="text-gray-300 mb-4">Demo users must use an access code or subscribe to upload videos</p>
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
                    <input type="file" id="videoFile" accept="video/*" class="mb-4 text-white file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-blue-600 file:text-white">
                    <br>
                    <p class="text-green-300 text-sm mb-4">✅ {user_plan.title()} Plan - Real analysis will be performed</p>
                    <button onclick="analyzeVideo()" id="analyzeBtn" 
                            class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-lg">
                        🤖 Analyze Techniques
                    </button>
                    {f'<p class="text-purple-300 text-xs mt-2">🎬 Elite plan: Video timestamps included!</p>' if user_plan == "elite" else ''}
                </div>
                ''' if user_plan != "demo" else ''}
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
            <div class="glass rounded-xl p-8 relative">
                {'' if user_plan != "demo" else '<div class="demo-badge">DEMO DATA</div>'}
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
                                <span class="text-gray-300">Triangle Ch
