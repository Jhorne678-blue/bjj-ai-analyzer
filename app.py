<div>
                                    <h3 class="text-lg font-semibold mb-4">Key Insights</h3>
                                    <div class="space-y-2">
                                        {_generate_insights_html(analysis_data.get('insights', []))}
                                    </div>
                                </div>
                            </div>
                            
                            <div class="mt-8">
                                <h3 class="text-lg font-semibold mb-4">Quality Metrics</h3>
                                <div class="grid md:grid-cols-4 gap-4">
                                    {_generate_quality_metrics_html(analysis_data.get('quality_metrics', {}))}
                                </div>
                            </div>
                        </div>
                        
                        <!-- Submissions Tab -->
                        <div id="submissions-tab" class="tab-content hidden">
                            <h2 class="text-2xl font-bold mb-6">Submissions Analysis</h2>
                            {_generate_technique_category_html(analysis_data.get('techniques', []), 'submissions', analysis_data.get('success_analytics', {}), analysis_data.get('failure_analytics', {}), plan_used)}
                        </div>
                        
                        <!-- Sweeps Tab -->
                        <div id="sweeps-tab" class="tab-content hidden">
                            <h2 class="text-2xl font-bold mb-6">Sweeps Analysis</h2>
                            {_generate_technique_category_html(analysis_data.get('techniques', []), 'sweeps', analysis_data.get('success_analytics', {}), analysis_data.get('failure_analytics', {}), plan_used)}
                        </div>
                        
                        <!-- Takedowns Tab -->
                        <div id="takedowns-tab" class="tab-content hidden">
                            <h2 class="text-2xl font-bold mb-6">Takedowns Analysis</h2>
                            {_generate_technique_category_html(analysis_data.get('techniques', []), 'takedowns', analysis_data.get('success_analytics', {}), analysis_data.get('failure_analytics', {}), plan_used)}
                        </div>
                        
                        <!-- Overall Tab -->
                        <div id="overall-tab" class="tab-content hidden">
                            <h2 class="text-2xl font-bold mb-6">Complete Technique List</h2>
                            {_generate_all_techniques_html(analysis_data.get('techniques', []))}
                        </div>
                    </div>
                </div>
            </div>
            
            <script>
            function showTab(tabName) {{
                // Hide all tab contents
                document.querySelectorAll('.tab-content').forEach(tab => {{
                    tab.classList.add('hidden');
                }});
                
                // Remove active class from all buttons
                document.querySelectorAll('.tab-button').forEach(btn => {{
                    btn.classList.remove('active', 'border-purple-500', 'text-purple-600');
                    btn.classList.add('border-transparent', 'text-gray-500');
                }});
                
                // Show selected tab
                document.getElementById(tabName + '-tab').classList.remove('hidden');
                
                // Add active class to clicked button
                event.target.classList.add('active', 'border-purple-500', 'text-purple-600');
                event.target.classList.remove('border-transparent', 'text-gray-500');
            }}
            </script>
        </body>
        </html>
        '''
        
    except Exception as e:
        logger.error(f"Analysis display error: {str(e)}")
        return redirect(url_for('dashboard'))

def _get_plan_color(plan):
    """Get color scheme for plan badges"""
    colors = {'free': 'gray', 'pro': 'purple', 'black_belt': 'yellow'}
    return colors.get(plan, 'gray')

def _generate_tier_analytics_display(analysis_data, plan):
    """Generate tier-specific analytics display"""
    if plan == 'free':
        return _generate_free_analytics_display(analysis_data)
    elif plan == 'pro':
        return _generate_pro_analytics_display(analysis_data)
    elif plan == 'black_belt':
        return _generate_black_belt_analytics_display(analysis_data)
    else:
        return ''

def _generate_free_analytics_display(analysis_data):
    """Generate basic analytics display for free tier"""
    free_analytics = analysis_data.get('free_analytics', {})
    
    return f'''
    <!-- Free Tier Analytics -->
    <div class="bg-gray-50 rounded-xl shadow-md p-6 mb-8">
        <h3 class="text-lg font-semibold text-gray-800 mb-4">📊 Basic Performance Summary</h3>
        <div class="grid md:grid-cols-3 gap-6">
            <div class="text-center">
                <div class="text-2xl font-bold text-green-600">{free_analytics.get('your_success_rate', 0)}%</div>
                <div class="text-sm text-gray-600">Your Success Rate</div>
            </div>
            <div class="text-center">
                <div class="text-2xl font-bold text-blue-600">{free_analytics.get('techniques_you_succeeded', 0)}</div>
                <div class="text-sm text-gray-600">Successful Techniques</div>
            </div>
            <div class="text-center">
                <div class="text-2xl font-bold text-red-600">{free_analytics.get('times_opponent_succeeded', 0)}</div>
                <div class="text-sm text-gray-600">Times Caught</div>
            </div>
        </div>
        
        <div class="mt-6 p-4 bg-purple-100 rounded-lg">
            <h4 class="font-semibold text-purple-800 mb-2">🚀 Unlock Advanced Analytics</h4>
            <p class="text-sm text-purple-700 mb-3">Get detailed position analysis, friend challenges, and AI coaching with Pro or Black Belt plans.</p>
            <a href="/upgrade" class="bg-purple-600 text-white px-4 py-2 rounded text-sm hover:bg-purple-700 transition-colors">
                Upgrade Now
            </a>
        </div>
    </div>
    '''

def _generate_pro_analytics_display(analysis_data):
    """Generate advanced analytics display for pro tier"""
    pro_analytics = analysis_data.get('pro_analytics', {})
    free_analytics = analysis_data.get('free_analytics', {})
    
    position_breakdown = pro_analytics.get('position_breakdown', {})
    weakest_positions = pro_analytics.get('weakest_positions', [])
    
    return f'''
    <!-- Pro Tier Analytics -->
    <div class="bg-blue-50 rounded-xl shadow-md p-6 mb-8">
        <h3 class="text-lg font-semibold text-blue-800 mb-6">📈 Advanced Performance Analytics</h3>
        
        <div class="grid md:grid-cols-2 gap-8 mb-6">
            <!-- Success Rate Overview -->
            <div>
                <h4 class="font-semibold mb-3">Performance Overview</h4>
                <div class="space-y-2">
                    <div class="flex justify-between">
                        <span>Your Success Rate:</span>
                        <strong class="text-green-600">{free_analytics.get('your_success_rate', 0)}%</strong>
                    </div>
                    <div class="flex justify-between">
                        <span>Successful Techniques:</span>
                        <strong>{free_analytics.get('techniques_you_succeeded', 0)}</strong>
                    </div>
                    <div class="flex justify-between">
                        <span>Times Caught:</span>
                        <strong class="text-red-600">{free_analytics.get('times_opponent_succeeded', 0)}</strong>
                    </div>
                </div>
            </div>
            
            <!-- Position Analysis -->
            <div>
                <h4 class="font-semibold mb-3">Position Performance</h4>
                <div class="space-y-2">
                    {_generate_position_breakdown_html(position_breakdown)}
                </div>
            </div>
        </div>
        
        <!-- Challenge Suggestions -->
        <div class="bg-white rounded-lg p-4">
            <h4 class="font-semibold text-green-800 mb-3">🏆 Recommended Challenges</h4>
            <div class="grid md:grid-cols-3 gap-4">
                {_generate_challenge_suggestions_html(pro_analytics.get('challenge_suggestions', []))}
            </div>
        </div>
    </div>
    '''

def _generate_black_belt_analytics_display(analysis_data):
    """Generate expert analytics display for black belt tier"""
    black_belt_analytics = analysis_data.get('black_belt_analytics', {})
    pro_analytics = analysis_data.get('pro_analytics', {})
    
    competition_readiness = black_belt_analytics.get('competition_readiness', {})
    technique_sequences = black_belt_analytics.get('technique_sequences', [])
    ai_predictions = black_belt_analytics.get('ai_predictions', [])
    
    return f'''
    <!-- Black Belt Tier Analytics -->
    <div class="bg-yellow-50 rounded-xl shadow-md p-6 mb-8">
        <h3 class="text-lg font-semibold text-yellow-800 mb-6">🥇 Elite Performance Analytics</h3>
        
        <div class="grid md:grid-cols-3 gap-6 mb-6">
            <!-- Competition Readiness -->
            <div class="bg-white rounded-lg p-4">
                <h4 class="font-semibold text-red-800 mb-3">🎯 Competition Readiness</h4>
                <div class="text-center">
                    <div class="text-3xl font-bold text-red-600">{competition_readiness.get('readiness_score', 0)}%</div>
                    <div class="text-sm text-gray-600">{competition_readiness.get('readiness_level', 'Unknown')}</div>
                </div>
            </div>
            
            <!-- AI Predictions -->
            <div class="bg-white rounded-lg p-4">
                <h4 class="font-semibold text-purple-800 mb-3">🧠 AI Insights</h4>
                <div class="space-y-2 text-sm">
                    {_generate_ai_predictions_html(ai_predictions)}
                </div>
            </div>
            
            <!-- Technique Sequences -->
            <div class="bg-white rounded-lg p-4">
                <h4 class="font-semibold text-blue-800 mb-3">🔗 Best Sequences</h4>
                <div class="space-y-2 text-sm">
                    {_generate_sequences_html(technique_sequences)}
                </div>
            </div>
        </div>
        
        <!-- Video Breakdown Points -->
        <div class="bg-white rounded-lg p-4 mb-4">
            <h4 class="font-semibold text-green-800 mb-3">📹 Frame-by-Frame Analysis</h4>
            <div class="space-y-3">
                {_generate_video_breakdown_html(black_belt_analytics.get('video_breakdown_points', []))}
            </div>
        </div>
        
        <!-- Master Coaching Recommendations -->
        <div class="bg-gradient-to-r from-yellow-400 to-orange-500 rounded-lg p-4 text-white">
            <h4 class="font-semibold mb-3">👨‍🏫 Master-Level Coaching</h4>
            <div class="grid md:grid-cols-2 gap-4">
                {_generate_coaching_recommendations_html(black_belt_analytics.get('coaching_recommendations', []))}
            </div>
        </div>
    </div>
    '''

def _generate_position_breakdown_html(position_breakdown):
    """Generate HTML for position performance breakdown"""
    if not position_breakdown:
        return '<p class="text-gray-500">No position data available</p>'
    
    html = ""
    for position, stats in list(position_breakdown.items())[:3]:  # Top 3 positions
        success_rate = (stats['your_success'] / max(stats['total'], 1)) * 100
        html += f'''
        <div class="flex justify-between items-center">
            <span class="text-sm">{position}:</span>
            <span class="font-medium {'text-green-600' if success_rate >= 50 else 'text-red-600'}">{success_rate:.0f}%</span>
        </div>
        '''
    return html

def _generate_challenge_suggestions_html(challenges):
    """Generate HTML for challenge suggestions"""
    html = ""
    for challenge in challenges[:3]:  # Top 3 challenges
        html += f'''
        <div class="p-3 bg-green-50 rounded border-l-4 border-green-500">
            <div class="text-sm font-medium">{challenge}</div>
        </div>
        '''
    return html

def _generate_ai_predictions_html(predictions):
    """Generate HTML for AI predictions"""
    if not predictions:
        return '<p class="text-gray-500">Analyzing patterns...</p>'
    
    html = ""
    for prediction in predictions:
        html += f'<div class="text-purple-700">• {prediction}</div>'
    return html

def _generate_sequences_html(sequences):
    """Generate HTML for technique sequences"""
    if not sequences:
        return '<p class="text-gray-500">No sequences detected</p>'
    
    html = ""
    for seq in sequences[:3]:  # Top 3 sequences
        html += f'''
        <div class="border-l-4 border-blue-500 pl-2">
            <div class="font-medium">{seq['first']} → {seq['second']}</div>
            <div class="text-xs text-gray-600">{seq['success_rate']} success rate</div>
        </div>
        '''
    return html

def _generate_video_breakdown_html(breakdown_points):
    """Generate HTML for video breakdown points"""
    if not breakdown_points:
        return '<p class="text-gray-500">No breakdown points available</p>'
    
    html = ""
    for point in breakdown_points:
        html += f'''
        <div class="border rounded p-3 hover:bg-gray-50">
            <div class="flex justify-between items-start">
                <div>
                    <span class="font-medium text-blue-600">{point['timestamp']}</span>
                    <span class="ml-2">{point['technique']}</span>
                </div>
                <span class="text-xs text-gray-500">{point['analysis']}</span>
            </div>
            <div class="text-sm text-gray-600 mt-1">{point['improvement_note']}</div>
        </div>
        '''
    return html

def _generate_coaching_recommendations_html(recommendations):
    """Generate HTML for coaching recommendations"""
    html = ""
    for rec in recommendations[:4]:  # Top 4 recommendations
        html += f'''
        <div class="bg-white bg-opacity-20 rounded p-3">
            <div class="text-sm font-medium">• {rec}</div>
        </div>
        '''
    return html

# PRESERVED: All existing HTML generation methods
def _generate_category_breakdown_html(category_breakdown):
    """Generate HTML for category breakdown"""
    html = ""
    for category, data in category_breakdown.items():
        category_name = category.replace('_', ' ').title()
        confidence_pct = data.get('avg_confidence', 0) * 100
        html += f'''
        <div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
            <div>
                <div class="font-medium">{category_name}</div>
                <div class="text-sm text-gray-500">{data.get('count', 0)} techniques</div>
            </div>
            <div class="text-right">
                <div class="font-bold text-purple-600">{confidence_pct:.1f}%</div>
                <div class="text-xs text-gray-500">avg confidence</div>
            </div>
        </div>
        '''
    return html

def _generate_insights_html(insights):
    """Generate HTML for insights"""
    html = ""
    for insight in insights:
        html += f'''
        <div class="flex items-start space-x-2">
            <div class="text-green-500 mt-1">✓</div>
            <div class="text-gray-700">{insight}</div>
        </div>
        '''
    return html

def _generate_quality_metrics_html(quality_metrics):
    """Generate HTML for quality metrics"""
    html = ""
    for metric, value in quality_metrics.items():
        metric_name = metric.replace('_', ' ').title()
        html += f'''
        <div class="text-center">
            <div class="text-2xl font-bold text-blue-600">{value}%</div>
            <div class="text-sm text-gray-600">{metric_name}</div>
        </div>
        '''
    return html

def _generate_technique_category_html(techniques, category, success_analytics, failure_analytics, plan='free'):
    """Generate HTML for specific technique category with tier-aware features"""
    category_techniques = [t for t in techniques if t.get('category') == category]
    
    if not category_techniques:
        return f'<p class="text-gray-500 text-center py-8">No {category} detected in this video.</p>'
    
    # Get success/failure data for this category (PRESERVED)
    success_data = success_analytics.get(category, [])
    failure_data = failure_analytics.get(category, [])
    
    # Tier-specific success/failure charts
    if plan != 'free':
        analytics_section = f'''
        <div class="grid md:grid-cols-2 gap-8 mb-8">
            <!-- Your Success Rates -->
            <div class="bg-green-50 rounded-lg p-6">
                <h3 class="text-lg font-semibold text-green-800 mb-4">📈 Your Success Rates (Best to Worst)</h3>
                {_generate_success_chart_html(success_data)}
            </div>
            
            <!-- What You Get Caught With -->
            <div class="bg-red-50 rounded-lg p-6">
                <h3 class="text-lg font-semibold text-red-800 mb-4">🎯 Most Caught With (Defend Better)</h3>
                {_generate_failure_chart_html(failure_data)}
            </div>
        </div>
        '''
    else:
        analytics_section = f'''
        <div class="bg-gray-100 rounded-lg p-6 mb-8">
            <h3 class="text-lg font-semibold text-gray-800 mb-4">📊 {category.replace('_', ' ').title()} Summary</h3>
            <p class="text-gray-600 mb-4">Upgrade to Pro or Black Belt for detailed success/failure analytics and position breakdowns.</p>
            <a href="/upgrade" class="bg-purple-600 text-white px-4 py-2 rounded text-sm hover:bg-purple-700 transition-colors">
                Unlock Advanced Analytics
            </a>
        </div>
        '''
    
    html = f'''
    {analytics_section}
    
    <div class="mb-6">
        <div class="text-lg text-gray-600 mb-4">All {len(category_techniques)} {category} techniques detected</div>
    </div>
    <div class="space-y-4">
    '''
    
    for tech in category_techniques:
        confidence_pct = tech.get('confidence', 0) * 100
        start_time = tech.get('start_time', 0)
        end_time = tech.get('end_time', 0)
        is_yours = tech.get('is_your_technique', True)
        outcome = tech.get('outcome', 'Unknown')
        
        # Color coding based on who did it and outcome (PRESERVED)
        if is_yours:
            outcome_class = 'bg-green-100 text-green-800' if outcome == 'Success' else 'bg-yellow-100 text-yellow-800'
            outcome_prefix = 'Your'
        else:
            outcome_class = 'bg-red-100 text-red-800' if outcome == 'Success' else 'bg-blue-100 text-blue-800'
            outcome_prefix = 'Opponent'
        
        html += f'''
        <div class="border border-gray-200 rounded-lg p-4">
            <div class="flex justify-between items-start mb-2">
                <h3 class="text-lg font-semibold">{tech.get('name', 'Unknown Technique')}</h3>
                <div class="flex space-x-2">
                    <span class="bg-purple-100 text-purple-800 text-sm px-2 py-1 rounded-full">{confidence_pct:.1f}%</span>
                    <span class="{outcome_class} text-sm px-2 py-1 rounded-full">{outcome_prefix} {outcome}</span>
                </div>
            </div>
            <div class="grid md:grid-cols-3 gap-4 text-sm">
                <div>
                    <span class="text-gray-500">Time:</span> {start_time:.1f}s - {end_time:.1f}s
                </div>
                <div>
                    <span class="text-gray-500">Position:</span> {tech.get('position', 'Unknown')}
                </div>
                <div>
                    <span class="text-gray-500">Quality Score:</span> {tech.get('quality_score', 0):.1f}/100
                </div>
            </div>
            <div class="mt-3">
                <div class="text-xs text-gray-500 mb-1">Execution Rating:</div>
                <span class="bg-{_get_rating_color(tech.get('execution_rating', ''))} text-white text-xs px-2 py-1 rounded">
                    {tech.get('execution_rating', 'Unknown')}
                </span>
            </div>
            <div class="mt-3 text-sm text-gray-600">
                <strong>{'Success Tip' if is_yours and outcome == 'Success' else 'Improvement Tip'}:</strong> 
                {tech.get('improvement_tips', 'Keep practicing this technique.')}
            </div>
        </div>
        '''
    
    html += '</div>'
    return html

# PRESERVED: All existing chart generation methods
def _generate_success_chart_html(success_data):
    """Generate HTML for success rate chart"""
    if not success_data:
        return '<p class="text-gray-500 text-center py-4">No data available for this session</p>'
    
    html = '<div class="space-y-3">'
    for i, data in enumerate(success_data[:5]):  # Top 5
        percentage = data['success_rate']
        attempts = data['attempts']
        successes = data['successes']
        
        # Color based on success rate
        if percentage >= 80:
            bar_color = 'bg-green-500'
            text_color = 'text-green-700'
        elif percentage >= 60:
            bar_color = 'bg-yellow-500'
            text_color = 'text-yellow-700'
        else:
            bar_color = 'bg-red-500'
            text_color = 'text-red-700'
        
        html += f'''
        <div class="relative">
            <div class="flex justify-between items-center mb-1">
                <span class="text-sm font-medium truncate">{data['technique']}</span>
                <span class="{text_color} text-sm font-bold">{percentage}%</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2">
                <div class="{bar_color} h-2 rounded-full" style="width: {percentage}%"></div>
            </div>
            <div class="text-xs text-gray-500 mt-1">{successes}/{attempts} attempts</div>
        </div>
        '''
    
    html += '</div>'
    return html

def _generate_failure_chart_html(failure_data):
    """Generate HTML for failure/caught rate chart"""
    if not failure_data:
        return '<p class="text-gray-500 text-center py-4">No data available for this session</p>'
    
    html = '<div class="space-y-3">'
    for i, data in enumerate(failure_data[:5]):  # Top 5
        percentage = data['caught_rate']
        attempts = data['attempts']
        caught = data['times_caught']
        
        # Color based on how often caught (red = bad, green = good defense)
        if percentage >= 80:
            bar_color = 'bg-red-500'
            text_color = 'text-red-700'
        elif percentage >= 60:
            bar_color = 'bg-orange-500'
            text_color = 'text-orange-700'
        elif percentage >= 40:
            bar_color = 'bg-yellow-500'
            text_color = 'text-yellow-700'
        else:
            bar_color = 'bg-green-500'
            text_color = 'text-green-700'
        
        html += f'''
        <div class="relative">
            <div class="flex justify-between items-center mb-1">
                <span class="text-sm font-medium truncate">{data['technique']}</span>
                <span class="{text_color} text-sm font-bold">{percentage}%</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2">
                <div class="{bar_color} h-2 rounded-full" style="width: {percentage}%"></div>
            </div>
            <div class="text-xs text-gray-500 mt-1">Caught {caught}/{attempts} times</div>
        </div>
        '''
    
    html += '</div>'
    return html

def _generate_all_techniques_html(techniques):
    """Generate HTML for all techniques overview"""
    if not techniques:
        return '<p class="text-gray-500 text-center py-8">No techniques detected in this video.</p>'
    
    html = f'''
    <div class="mb-6">
        <div class="text-lg text-gray-600 mb-4">Complete analysis of all {len(techniques)} detected techniques</div>
    </div>
    <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
                <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Technique</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Category</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Time</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Confidence</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Quality</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Rating</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Outcome</th>
                </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
    '''
    
    for tech in techniques:
        confidence_pct = tech.get('confidence', 0) * 100
        category_name = tech.get('category', '').replace('_', ' ').title()
        is_yours = tech.get('is_your_technique', True)
        outcome = tech.get('outcome', 'Unknown')
        
        # Color coding for outcome
        if is_yours:
            outcome_class = 'bg-green-100 text-green-800' if outcome == 'Success' else 'bg-yellow-100 text-yellow-800'
            outcome_text = f'Your {outcome}'
        else:
            outcome_class = 'bg-red-100 text-red-800' if outcome == 'Success' else 'bg-blue-100 text-blue-800'
            outcome_text = f'Opponent {outcome}'
        
        html += f'''
                <tr>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{tech.get('name', 'Unknown')}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{category_name}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{tech.get('start_time', 0):.1f}s</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{confidence_pct:.1f}%</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{tech.get('quality_score', 0):.1f}/100</td>
                    <td class="px-6 py-4 whitespace-nowrap">
                        <span class="bg-{_get_rating_color(tech.get('execution_rating', ''))} text-white text-xs px-2 py-1 rounded">
                            {tech.get('execution_rating', 'Unknown')}
                        </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                        <span class="{outcome_class} text-xs px-2 py-1 rounded">
                            {outcome_text}
                        </span>
                    </td>
                </tr>
        '''
    
    html += '''
            </tbody>
        </table>
    </div>
    '''
    return html

def _get_rating_color(rating):
    """Get Tailwind color class for execution rating"""
    rating_colors = {
        'Excellent': 'green-500',
        'Good': 'blue-500',
        'Fair': 'yellow-500',
        'Needs Work': 'red-500'
    }
    return rating_colors.get(rating, 'gray-500')

# Add these methods to the app for the HTML generation
app._generate_category_breakdown_html = _generate_category_breakdown_html
app._generate_insights_html = _generate_insights_html
app._generate_quality_metrics_html = _generate_quality_metrics_html
app._generate_technique_category_html = _generate_technique_category_html
app._generate_all_techniques_html = _generate_all_techniques_html
app._generate_success_chart_html = _generate_success_chart_html
app._generate_failure_chart_html = _generate_failure_chart_html
app._get_rating_color = _get_rating_color
app._get_plan_color = _get_plan_color
app._generate_tier_analytics_display = _generate_tier_analytics_display

# Initialize database on startup
try:
    init_database()
except Exception as e:
    logger.error(f"Database initialization failed: {str(e)}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)# PRESERVED: All existing analysis results route with tier enhancements
@app.route('/analysis/<int:video_id>')
def analysis_results(video_id):
    """Display comprehensive analysis results with tier-specific features"""
    try:
        if 'user_id' not in session:
            return redirect(url_for('auth'))
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Get video and analysis data
        cursor.execute('''
            SELECT * FROM videos WHERE id = ? AND user_id = ?
        ''', (video_id, session['user_id']))
        
        video = cursor.fetchone()
        if not video:
            return redirect(url_for('dashboard'))
        
        analysis_data = json.loads(video['analysis_data'])
        plan_used = video.get('plan_used', 'free')
        conn.close()
        
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Analysis Results - BJJ AI Analyzer</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <script src="https://cdn.tailwindcss.com"></script>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body class="bg-gray-50">
            <div class="min-h-screen">
                <nav class="bg-white shadow-lg">
                    <div class="max-w-7xl mx-auto px-4">
                        <div class="flex justify-between items-center h-16">
                            <div class="flex items-center">
                                <span class="text-xl font-bold text-gray-800">🥋 BJJ AI Analyzer</span>
                            </div>
                            <div class="flex items-center space-x-4">
                                <span class="bg-{_get_plan_color(plan_used)}-100 text-{_get_plan_color(plan_used)}-800 px-3 py-1 rounded-full text-sm">
                                    {TIER_PRICING[plan_used]['name']} Analysis
                                </span>
                                <a href="/dashboard" class="text-purple-600 hover:text-purple-800">← Back to Dashboard</a>
                            </div>
                        </div>
                    </div>
                </nav>
                
                <div class="max-w-7xl mx-auto px-4 py-8">
                    <div class="mb-8">
                        <h1 class="text-3xl font-bold text-gray-900 mb-2">Analysis Results</h1>
                        <p class="text-gray-600">Video: {video['original_filename']}</p>
                        <p class="text-sm text-gray-500">Analyzed on {video['upload_timestamp']} using {TIER_PRICING[plan_used]['name']} features</p>
                    </div>
                    
                    <!-- Summary Cards -->
                    <div class="grid md:grid-cols-4 gap-6 mb-8">
                        <div class="bg-white rounded-xl shadow-md p-6 text-center">
                            <div class="text-3xl font-bold text-purple-600">{analysis_data.get('total_techniques', 0)}</div>
                            <div class="text-sm text-gray-600">Total Techniques</div>
                        </div>
                        <div class="bg-white rounded-xl shadow-md p-6 text-center">
                            <div class="text-3xl font-bold text-green-600">{analysis_data.get('average_confidence', 0):.1%}</div>
                            <div class="text-sm text-gray-600">Avg Confidence</div>
                        </div>
                        <div class="bg-white rounded-xl shadow-md p-6 text-center">
                            <div class="text-3xl font-bold text-blue-600">{analysis_data.get('duration', 0):.1f}s</div>
                            <div class="text-sm text-gray-600">Video Duration</div>
                        </div>
                        <div class="bg-white rounded-xl shadow-md p-6 text-center">
                            <div class="text-3xl font-bold text-yellow-600">{analysis_data.get('techniques_per_minute', 0):.1f}</div>
                            <div class="text-sm text-gray-600">Techniques/Min</div>
                        </div>
                    </div>
                    
                    <!-- Tier-Specific Analytics Section -->
                    {_generate_tier_analytics_display(analysis_data, plan_used)}
                    
                    <!-- Tabs Navigation -->
                    <div class="bg-white rounded-t-xl shadow-md">
                        <div class="border-b border-gray-200">
                            <nav class="flex space-x-8 px-6" aria-label="Tabs">
                                <button onclick="showTab('overview')" class="tab-button active border-b-2 border-purple-500 py-4 px-1 text-sm font-medium text-purple-600">
                                    Overview
                                </button>
                                <button onclick="showTab('submissions')" class="tab-button border-b-2 border-transparent py-4 px-1 text-sm font-medium text-gray-500 hover:text-gray-700">
                                    Submissions
                                </button>
                                <button onclick="showTab('sweeps')" class="tab-button border-b-2 border-transparent py-4 px-1 text-sm font-medium text-gray-500 hover:text-gray-700">
                                    Sweeps
                                </button>
                                <button onclick="showTab('takedowns')" class="tab-button border-b-2 border-transparent py-4 px-1 text-sm font-medium text-gray-500 hover:text-gray-700">
                                    Takedowns
                                </button>
                                <button onclick="showTab('overall')" class="tab-button border-b-2 border-transparent py-4 px-1 text-sm font-medium text-gray-500 hover:text-gray-700">
                                    Overall Stats
                                </button>
                            </nav>
                        </div>
                    </div>
                    
                    <!-- Tab Content -->
                    <div class="bg-white rounded-b-xl shadow-md p-6">
                        <!-- Overview Tab -->
                        <div id="overview-tab" class="tab-content">
                            <h2 class="text-2xl font-bold mb-6">Training Session Overview</h2>
                            
                            <div class="grid md:grid-cols-2 gap-8">
                                <div>
                                    <h3 class="text-lg font-semibold mb-4">Category Breakdown</h3>
                                    <div class="space-y-3">
                                        {_generate_category_breakdown_html(analysis_data.get('category_breakdown', {}))}
                                    </div>
                                </div>
                                
                                <div>
                                    <hfrom flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import os
import json
import secrets
import logging
from datetime import datetime, timedelta
from analyzer import BJJAnalyzer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'bjj-ai-analyzer-secret-key-2024')

# Configuration
UPLOAD_FOLDER = 'uploads'
DATABASE = 'bjj_analyzer.db'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize BJJ Analyzer
bjj_analyzer = BJJAnalyzer()

# NEW: Tier pricing configuration
TIER_PRICING = {
    'free': {'price': 0, 'uploads_per_month': 1, 'name': 'Free'},
    'pro': {'price': 19.99, 'uploads_per_month': 4, 'name': 'Pro'},
    'black_belt': {'price': 49.99, 'uploads_per_month': 12, 'name': 'Black Belt'}
}

def init_database():
    """Initialize SQLite database with tier system"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Enhanced Users table with tier tracking
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            plan TEXT DEFAULT 'free',
            plan_expires TIMESTAMP NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_uploads INTEGER DEFAULT 0,
            uploads_this_month INTEGER DEFAULT 0,
            last_upload_reset TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            points INTEGER DEFAULT 0,
            friend_code TEXT UNIQUE,
            friends TEXT DEFAULT '[]',
            challenges_completed INTEGER DEFAULT 0
        )
    ''')
    
    # Enhanced Videos table (PRESERVED all existing fields)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT,
            original_filename TEXT,
            upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            analysis_complete BOOLEAN DEFAULT FALSE,
            analysis_data TEXT,
            total_techniques INTEGER DEFAULT 0,
            average_confidence REAL DEFAULT 0.0,
            duration REAL DEFAULT 0.0,
            plan_used TEXT DEFAULT 'free',
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # NEW: Challenges table for Pro/Black Belt features
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS challenges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            challenge_type TEXT NOT NULL,
            challenge_data TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP NULL,
            points_awarded INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # NEW: Friend connections table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS friend_connections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            friend_id INTEGER NOT NULL,
            connected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (friend_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    logger.info("Database initialized successfully with tier system")

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_upload_limit(user_id, plan):
    """Check if user has reached their monthly upload limit"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get user's upload data
    cursor.execute('''
        SELECT uploads_this_month, last_upload_reset, plan 
        FROM users WHERE id = ?
    ''', (user_id,))
    
    user_data = cursor.fetchone()
    if not user_data:
        conn.close()
        return False, "User not found"
    
    uploads_this_month = user_data['uploads_this_month']
    last_reset = datetime.fromisoformat(user_data['last_upload_reset']) if user_data['last_upload_reset'] else datetime.now()
    current_plan = user_data['plan']
    
    # Check if we need to reset monthly counter
    now = datetime.now()
    if now.month != last_reset.month or now.year != last_reset.year:
        # Reset monthly counter
        cursor.execute('''
            UPDATE users SET uploads_this_month = 0, last_upload_reset = ? 
            WHERE id = ?
        ''', (now.isoformat(), user_id))
        uploads_this_month = 0
        conn.commit()
    
    conn.close()
    
    # Check limits based on plan
    plan_limits = TIER_PRICING.get(current_plan, TIER_PRICING['free'])
    monthly_limit = plan_limits['uploads_per_month']
    
    if uploads_this_month >= monthly_limit:
        return False, f"Monthly upload limit reached ({monthly_limit} uploads for {plan_limits['name']} plan)"
    
    return True, f"{uploads_this_month + 1}/{monthly_limit} uploads this month"

def increment_upload_count(user_id):
    """Increment user's monthly upload count"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE users SET 
            uploads_this_month = uploads_this_month + 1,
            total_uploads = total_uploads + 1
        WHERE id = ?
    ''', (user_id,))
    
    conn.commit()
    conn.close()

def generate_friend_code():
    """Generate unique friend code"""
    import string
    import random
    
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE friend_code = ?', (code,))
        if not cursor.fetchone():
            conn.close()
            return code
        conn.close()

def login_required(f):
    """Decorator to require login"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth'))
        return f(*args, **kwargs)
    return decorated_function

# Routes (PRESERVED all existing routes)
@app.route('/')
def index():
    """Enhanced landing page with tier information"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>BJJ AI Analyzer</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-50">
        <div class="min-h-screen">
            <!-- Hero Section -->
            <div class="flex items-center justify-center py-20">
                <div class="max-w-4xl w-full text-center px-4">
                    <h1 class="text-5xl font-bold text-gray-900 mb-4">🥋 BJJ AI Analyzer</h1>
                    <p class="text-xl text-gray-600 mb-8">Professional Brazilian Jiu-Jitsu Video Analysis with 100+ Techniques</p>
                    <a href="/auth" class="bg-purple-600 text-white px-8 py-4 rounded-lg hover:bg-purple-700 transition-colors text-lg">
                        Start Free Trial
                    </a>
                </div>
            </div>
            
            <!-- Pricing Tiers -->
            <div class="max-w-7xl mx-auto px-4 py-16">
                <h2 class="text-3xl font-bold text-center mb-12">Choose Your Plan</h2>
                <div class="grid md:grid-cols-3 gap-8">
                    
                    <!-- Free Tier -->
                    <div class="bg-white rounded-xl shadow-lg p-8 border-2 border-gray-200">
                        <div class="text-center">
                            <h3 class="text-2xl font-bold text-gray-900 mb-2">Free</h3>
                            <div class="text-4xl font-bold text-gray-600 mb-4">$0<span class="text-lg">/month</span></div>
                            <p class="text-gray-600 mb-6">Perfect for trying out BJJ analysis</p>
                        </div>
                        <ul class="space-y-3 mb-8">
                            <li class="flex items-center"><span class="text-green-500 mr-2">✓</span>1 video upload per month</li>
                            <li class="flex items-center"><span class="text-green-500 mr-2">✓</span>Basic technique detection</li>
                            <li class="flex items-center"><span class="text-green-500 mr-2">✓</span>Simple success/failure stats</li>
                            <li class="flex items-center"><span class="text-green-500 mr-2">✓</span>8 techniques analyzed</li>
                        </ul>
                        <a href="/auth" class="block w-full bg-gray-600 text-white text-center py-3 rounded-lg hover:bg-gray-700 transition-colors">
                            Get Started Free
                        </a>
                    </div>
                    
                    <!-- Pro Tier -->
                    <div class="bg-white rounded-xl shadow-lg p-8 border-2 border-purple-500 relative">
                        <div class="absolute -top-4 left-1/2 transform -translate-x-1/2">
                            <span class="bg-purple-500 text-white px-4 py-1 rounded-full text-sm">POPULAR</span>
                        </div>
                        <div class="text-center">
                            <h3 class="text-2xl font-bold text-gray-900 mb-2">Pro</h3>
                            <div class="text-4xl font-bold text-purple-600 mb-4">$19.99<span class="text-lg">/month</span></div>
                            <p class="text-gray-600 mb-6">For serious BJJ practitioners</p>
                        </div>
                        <ul class="space-y-3 mb-8">
                            <li class="flex items-center"><span class="text-green-500 mr-2">✓</span>4 video uploads per month</li>
                            <li class="flex items-center"><span class="text-green-500 mr-2">✓</span>Advanced position analysis</li>
                            <li class="flex items-center"><span class="text-green-500 mr-2">✓</span>Friend connections & challenges</li>
                            <li class="flex items-center"><span class="text-green-500 mr-2">✓</span>Progress tracking</li>
                            <li class="flex items-center"><span class="text-green-500 mr-2">✓</span>20 techniques analyzed</li>
                            <li class="flex items-center"><span class="text-green-500 mr-2">✓</span>Daily/Weekly challenges</li>
                        </ul>
                        <a href="/auth" class="block w-full bg-purple-600 text-white text-center py-3 rounded-lg hover:bg-purple-700 transition-colors">
                            Start Pro Trial
                        </a>
                    </div>
                    
                    <!-- Black Belt Tier -->
                    <div class="bg-white rounded-xl shadow-lg p-8 border-2 border-yellow-500">
                        <div class="text-center">
                            <h3 class="text-2xl font-bold text-gray-900 mb-2">Black Belt</h3>
                            <div class="text-4xl font-bold text-yellow-600 mb-4">$49.99<span class="text-lg">/month</span></div>
                            <p class="text-gray-600 mb-6">Elite analysis for competitors</p>
                        </div>
                        <ul class="space-y-3 mb-8">
                            <li class="flex items-center"><span class="text-green-500 mr-2">✓</span>12 video uploads per month</li>
                            <li class="flex items-center"><span class="text-green-500 mr-2">✓</span>AI technique sequences</li>
                            <li class="flex items-center"><span class="text-green-500 mr-2">✓</span>Competition readiness</li>
                            <li class="flex items-center"><span class="text-green-500 mr-2">✓</span>Master-level coaching</li>
                            <li class="flex items-center"><span class="text-green-500 mr-2">✓</span>40 techniques analyzed</li>
                            <li class="flex items-center"><span class="text-green-500 mr-2">✓</span>Video breakdowns</li>
                        </ul>
                        <a href="/auth" class="block w-full bg-yellow-600 text-white text-center py-3 rounded-lg hover:bg-yellow-700 transition-colors">
                            Go Black Belt
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/auth')
def auth():
    """Authentication page (PRESERVED)"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login - BJJ AI Analyzer</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-50">
        <div class="min-h-screen flex items-center justify-center">
            <div class="max-w-md w-full bg-white rounded-lg shadow-xl p-8">
                <h2 class="text-2xl font-bold text-center mb-6">BJJ AI Analyzer</h2>
                
                <!-- Signup Form -->
                <form id="signup-form" class="space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Username</label>
                        <input type="text" name="username" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Email</label>
                        <input type="email" name="email" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Password</label>
                        <input type="password" name="password" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Plan</label>
                        <select name="plan" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md">
                            <option value="free">Free - $0/month</option>
                            <option value="pro">Pro - $19.99/month</option>
                            <option value="black_belt">Black Belt - $49.99/month</option>
                        </select>
                    </div>
                    <button type="submit" class="w-full bg-purple-600 text-white py-2 px-4 rounded-md hover:bg-purple-700">
                        Create Account
                    </button>
                </form>
                
                <div class="mt-4 text-center">
                    <a href="/dashboard" class="text-purple-600 hover:text-purple-800">Already have an account? Go to Dashboard</a>
                </div>
            </div>
        </div>
        
        <script>
        document.getElementById('signup-form').addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            
            try {
                const response = await fetch('/signup', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(Object.fromEntries(formData))
                });
                
                const result = await response.json();
                
                if (result.success) {
                    alert('Account created successfully!');
                    window.location.href = '/dashboard';
                } else {
                    alert(result.message);
                }
            } catch (error) {
                alert('Signup failed. Please try again.');
            }
        });
        </script>
    </body>
    </html>
    '''

@app.route('/signup', methods=['POST'])
def signup():
    """Enhanced user registration with tier selection"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        plan = data.get('plan', 'free')
        
        if not username or not email or not password:
            return jsonify({'success': False, 'message': 'All fields required'})
        
        if plan not in TIER_PRICING:
            plan = 'free'
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute('SELECT id FROM users WHERE username = ? OR email = ?', (username, email))
        if cursor.fetchone():
            conn.close()
            return jsonify({'success': False, 'message': 'Username or email already exists'})
        
        # Generate friend code
        friend_code = generate_friend_code()
        
        # Create user with tier information
        password_hash = generate_password_hash(password)
        plan_expires = None
        if plan != 'free':
            plan_expires = (datetime.now() + timedelta(days=30)).isoformat()
        
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, plan, plan_expires, friend_code)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, email, password_hash, plan, plan_expires, friend_code))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Set session
        session['user_id'] = user_id
        session['username'] = username
        session['plan'] = plan
        session['friend_code'] = friend_code
        
        return jsonify({'success': True, 'message': f'Account created successfully with {TIER_PRICING[plan]["name"]} plan!'})
        
    except Exception as e:
        logger.error(f"Signup error: {str(e)}")
        return jsonify({'success': False, 'message': 'Registration failed'})

@app.route('/dashboard')
def dashboard():
    """Enhanced dashboard with tier-specific features and upload limits"""
    if 'user_id' not in session:
        return redirect(url_for('auth'))
    
    # Get user data including upload limits
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT username, plan, uploads_this_month, total_uploads, friend_code, friends
        FROM users WHERE id = ?
    ''', (session['user_id'],))
    
    user_data = cursor.fetchone()
    if not user_data:
        conn.close()
        return redirect(url_for('auth'))
    
    plan = user_data['plan']
    uploads_this_month = user_data['uploads_this_month']
    total_uploads = user_data['total_uploads']
    friend_code = user_data['friend_code']
    
    # Get plan limits
    plan_info = TIER_PRICING.get(plan, TIER_PRICING['free'])
    monthly_limit = plan_info['uploads_per_month']
    uploads_remaining = monthly_limit - uploads_this_month
    
    conn.close()
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard - BJJ AI Analyzer</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-50">
        <div class="min-h-screen">
            <nav class="bg-white shadow-lg">
                <div class="max-w-7xl mx-auto px-4">
                    <div class="flex justify-between items-center h-16">
                        <div class="flex items-center">
                            <span class="text-xl font-bold text-gray-800">🥋 BJJ AI Analyzer</span>
                        </div>
                        <div class="flex items-center space-x-4">
                            <span class="text-sm text-gray-600">Plan: {plan_info['name']}</span>
                            {('<a href="/upgrade" class="bg-purple-600 text-white px-4 py-2 rounded text-sm hover:bg-purple-700">Upgrade</a>' if plan == 'free' else '')}
                            <a href="/friends" class="text-purple-600 hover:text-purple-800">Friends</a>
                            <span class="text-sm text-gray-600">Welcome, {user_data['username']}!</span>
                        </div>
                    </div>
                </div>
            </nav>
            
            <div class="max-w-7xl mx-auto px-4 py-8">
                <h1 class="text-3xl font-bold text-gray-900 mb-8">Dashboard</h1>
                
                <!-- Tier Status & Upload Limits -->
                <div class="grid md:grid-cols-4 gap-6 mb-8">
                    <div class="bg-white rounded-xl shadow-md p-6">
                        <div class="text-2xl font-bold text-purple-600">{total_uploads}</div>
                        <div class="text-sm text-gray-600">Total Videos</div>
                    </div>
                    <div class="bg-white rounded-xl shadow-md p-6">
                        <div class="text-2xl font-bold text-{'green' if uploads_remaining > 0 else 'red'}-600">{uploads_remaining}</div>
                        <div class="text-sm text-gray-600">Uploads Remaining</div>
                    </div>
                    <div class="bg-white rounded-xl shadow-md p-6">
                        <div class="text-2xl font-bold text-blue-600">{uploads_this_month}/{monthly_limit}</div>
                        <div class="text-sm text-gray-600">This Month</div>
                    </div>
                    <div class="bg-white rounded-xl shadow-md p-6">
                        <div class="text-2xl font-bold text-yellow-600">{plan_info['name']}</div>
                        <div class="text-sm text-gray-600">Current Plan</div>
                    </div>
                </div>
                
                <!-- Upload Section -->
                <div class="bg-white rounded-xl shadow-md p-8 mb-8">
                    <h2 class="text-xl font-semibold mb-4">Upload BJJ Training Video</h2>
                    
                    {f'<div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">You have reached your monthly upload limit of {monthly_limit} videos. <a href="/upgrade" class="underline">Upgrade your plan</a> for more uploads.</div>' if uploads_remaining <= 0 else ''}
                    
                    <div id="upload-area" class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center cursor-pointer hover:border-purple-400 transition-colors {'opacity-50 cursor-not-allowed' if uploads_remaining <= 0 else ''}">
                        <div class="text-4xl mb-4">🎥</div>
                        <p class="text-lg text-gray-600 mb-2">
                            {'Upload limit reached - upgrade to continue' if uploads_remaining <= 0 else 'Click to upload or drag and drop your BJJ training video'}
                        </p>
                        <p class="text-sm text-gray-500">MP4, AVI, MOV supported (max 500MB)</p>
                        <input type="file" id="video-input" accept=".mp4,.avi,.mov,.mkv,.webm" class="hidden" {'disabled' if uploads_remaining <= 0 else ''}>
                        <div id="upload-progress" class="hidden mt-4">
                            <div class="bg-gray-200 rounded-full h-2">
                                <div id="progress-bar" class="bg-purple-600 h-2 rounded-full" style="width: 0%"></div>
                            </div>
                            <p class="text-sm text-gray-600 mt-2">Uploading and analyzing...</p>
                        </div>
                    </div>
                </div>
                
                <!-- Pro/Black Belt Features -->
                {_generate_tier_features_html(plan, friend_code) if plan != 'free' else _generate_upgrade_prompt_html()}
                
                <div id="recent-videos" class="bg-white rounded-xl shadow-md p-8">
                    <h2 class="text-xl font-semibold mb-4">Recent Analyses</h2>
                    <div id="video-list" class="space-y-4">
                        <p class="text-gray-500 text-center py-4">No videos uploaded yet. Upload your first BJJ training video to get started!</p>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
        const uploadArea = document.getElementById('upload-area');
        const videoInput = document.getElementById('video-input');
        const uploadProgress = document.getElementById('upload-progress');
        const progressBar = document.getElementById('progress-bar');
        const uploadsRemaining = {uploads_remaining};
        
        if (uploadsRemaining > 0) {{
            // Click to upload
            uploadArea.addEventListener('click', () => videoInput.click());
            
            // Drag and drop functionality
            uploadArea.addEventListener('dragover', (e) => {{
                e.preventDefault();
                uploadArea.classList.add('border-purple-400', 'bg-purple-50');
            }});
            
            uploadArea.addEventListener('dragleave', () => {{
                uploadArea.classList.remove('border-purple-400', 'bg-purple-50');
            }});
            
            uploadArea.addEventListener('drop', (e) => {{
                e.preventDefault();
                uploadArea.classList.remove('border-purple-400', 'bg-purple-50');
                const files = e.dataTransfer.files;
                if (files.length > 0) {{
                    handleFileUpload(files[0]);
                }}
            }});
            
            // File input change
            videoInput.addEventListener('change', (e) => {{
                if (e.target.files.length > 0) {{
                    handleFileUpload(e.target.files[0]);
                }}
            }});
        }}
