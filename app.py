#!/usr/bin/env python3
"""
Job4Freshers AI Chatbot - Flask API Server

This module provides REST API endpoints for the chatbot functionality
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import logging
import os
from datetime import datetime
import json

# Import our custom modules
from scraper import Job4Fresherscraper
from job_matcher import JobMatchingEngine
from chatbot import ChatbotConversationManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Initialize chatbot components
scraper = Job4Fresherscraper()
job_matcher = JobMatchingEngine()
chatbot = ChatbotConversationManager(job_matcher)

# Store active chat sessions
chat_sessions = {}

@app.route('/')
def index():
    """Serve the main chat interface"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        message = data['message']
        session_id = data.get('session_id', 'default')
        
        # Get or create chat session
        if session_id not in chat_sessions:
            chat_sessions[session_id] = ChatbotConversationManager(job_matcher)
        
        chatbot_session = chat_sessions[session_id]
        
        # Generate response
        response = chatbot_session.generate_response(message)
        
        # Format response for API
        api_response = {
            'status': 'success',
            'response': response['message'],
            'jobs': response['jobs'],
            'suggestions': response['suggestions'],
            'intent': response['intent'],
            'timestamp': response['timestamp']
        }
        
        return jsonify(api_response)
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/jobs/search', methods=['POST'])
def search_jobs():
    """Search for jobs based on query"""
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({'error': 'Query is required'}), 400
        
        query = data['query']
        limit = data.get('limit', 10)
        
        # Search for jobs
        jobs = job_matcher.find_matching_jobs(query, top_k=limit)
        
        return jsonify({
            'status': 'success',
            'query': query,
            'jobs': jobs,
            'count': len(jobs)
        })
        
    except Exception as e:
        logger.error(f"Error in job search endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/jobs/recommendations', methods=['POST'])
def get_recommendations():
    """Get job recommendations based on user profile"""
    try:
        data = request.get_json()
        
        if not data or 'profile' not in data:
            return jsonify({'error': 'User profile is required'}), 400
        
        profile = data['profile']
        limit = data.get('limit', 5)
        
        # Get recommendations
        recommendations = job_matcher.get_job_recommendations(profile, top_k=limit)
        
        return jsonify({
            'status': 'success',
            'profile': profile,
            'recommendations': recommendations,
            'count': len(recommendations)
        })
        
    except Exception as e:
        logger.error(f"Error in recommendations endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/jobs/statistics', methods=['GET'])
def get_job_statistics():
    """Get job market statistics"""
    try:
        stats = job_matcher.get_job_statistics()
        
        return jsonify({
            'status': 'success',
            'statistics': stats
        })
        
    except Exception as e:
        logger.error(f"Error in statistics endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/scrape', methods=['POST'])
def trigger_scraping():
    """Trigger job scraping process using sitemap-based approach"""
    try:
        data = request.get_json()
        max_jobs = data.get('max_jobs', None) if data else None
        full_extraction = data.get('full_extraction', False) if data else False
        
        if full_extraction:
            # Run comprehensive sitemap-based extraction
            jobs = scraper.run_full_extraction()
            message = f'Full sitemap-based extraction completed. Found {len(jobs)} jobs.'
        else:
            # Run limited sitemap-based scraper
            jobs = scraper.run_scraper(max_jobs=max_jobs)
            message = f'Sitemap-based scraping completed. Found {len(jobs)} jobs.'
        
        # Reload job matcher with new data
        job_matcher.load_job_data()
        
        return jsonify({
            'status': 'success',
            'message': message,
            'jobs_count': len(jobs),
            'extraction_type': 'full' if full_extraction else 'limited',
            'method': 'sitemap-based'
        })
        
    except Exception as e:
        logger.error(f"Error in scraping endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/scrape/full', methods=['POST'])
def trigger_full_extraction():
    """Trigger comprehensive sitemap-based job extraction"""
    try:
        # Run full sitemap-based extraction
        jobs = scraper.run_full_extraction()
        
        # Reload job matcher with new data
        job_matcher.load_job_data()
        
        # Get statistics
        stats = scraper.get_job_statistics()
        
        return jsonify({
            'status': 'success',
            'message': f'Full sitemap-based extraction completed. Extracted {len(jobs)} jobs.',
            'jobs_extracted': len(jobs),
            'total_jobs': stats.get('total_jobs', 0),
            'top_companies': dict(list(stats.get('top_companies', {}).items())[:5]),
            'top_locations': dict(list(stats.get('top_locations', {}).items())[:5]),
            'method': 'sitemap-based'
        })
        
    except Exception as e:
        logger.error(f"Error in full extraction endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/jobs/stats', methods=['GET'])
def get_detailed_job_statistics():
    """Get detailed job statistics"""
    try:
        stats = scraper.get_job_statistics()
        
        return jsonify({
            'status': 'success',
            'statistics': stats
        })
        
    except Exception as e:
        logger.error(f"Error in detailed statistics endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/chat/history/<session_id>', methods=['GET'])
def get_chat_history(session_id):
    """Get chat history for a session"""
    try:
        if session_id in chat_sessions:
            history = chat_sessions[session_id].get_conversation_history()
            return jsonify({
                'status': 'success',
                'session_id': session_id,
                'history': history
            })
        else:
            return jsonify({
                'status': 'success',
                'session_id': session_id,
                'history': []
            })
            
    except Exception as e:
        logger.error(f"Error getting chat history: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/chat/reset/<session_id>', methods=['POST'])
def reset_chat_session(session_id):
    """Reset a chat session"""
    try:
        if session_id in chat_sessions:
            chat_sessions[session_id].reset_conversation()
        
        return jsonify({
            'status': 'success',
            'message': f'Chat session {session_id} reset successfully'
        })
        
    except Exception as e:
        logger.error(f"Error resetting chat session: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'services': {
            'scraper': 'available',
            'job_matcher': 'available',
            'chatbot': 'available'
        }
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Create static directory if it doesn't exist
    if not os.path.exists('static'):
        os.makedirs('static')
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)