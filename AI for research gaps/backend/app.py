from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import logging
from datetime import datetime

from research_analyzer import ResearchAnalyzer
from config import Config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, 
            static_folder='../frontend',
            template_folder='../frontend')

app.config.from_object(Config)

# Initialize analyzer
analyzer = ResearchAnalyzer()

# Serve frontend files
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# API Routes
@app.route('/api/analyze', methods=['POST'])
def analyze_research():
    """Analyze research topic and identify gaps"""
    try:
        # Try to get JSON data
        if request.is_json:
            data = request.get_json()
        else:
            # Try to parse raw data
            try:
                data = json.loads(request.data)
            except:
                data = {}
        
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({
                'error': 'Query is required',
                'success': False
            }), 400
        
        logger.info(f"Processing query: {query}")
        
        # Perform analysis
        analysis = analyzer.generate_comprehensive_analysis(query)
        
        # Format response
        response = {
            'success': True,
            'query': query,
            'analysis': analysis,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in analyze endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/search', methods=['POST'])
def search_papers():
    """Search for research papers"""
    try:
        if request.is_json:
            data = request.get_json()
        else:
            try:
                data = json.loads(request.data)
            except:
                data = {}
        
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({
                'error': 'Query is required',
                'success': False
            }), 400
        
        logger.info(f"Searching for: {query}")
        
        # Search papers
        papers = analyzer.search_all_sources(query, max_per_source=3)
        
        # Extract trends
        trends = analyzer.analyze_trends(papers)
        
        return jsonify({
            'success': True,
            'query': query,
            'papers': papers,
            'trends': trends,
            'total_papers': len(papers),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in search endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/test', methods=['GET', 'POST'])
def test_endpoint():
    """Test endpoint for debugging"""
    if request.method == 'POST':
        logger.info(f"POST data: {request.data}")
        logger.info(f"POST json: {request.get_json(silent=True)}")
        logger.info(f"POST form: {request.form}")
    
    return jsonify({
        'success': True,
        'method': request.method,
        'data': str(request.data),
        'json': request.get_json(silent=True),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Research Intelligence Platform',
        'version': '1.0',
        'timestamp': datetime.now().isoformat()
    })

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({
        'error': 'Endpoint not found',
        'success': False
    }), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({
        'error': 'Internal server error',
        'success': False
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])