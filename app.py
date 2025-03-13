from flask import Flask, request, jsonify, render_template, session
import os
import json
from utils.image_analyzer import analyze_image
from utils.query_processor import QueryProcessor, direct_image_query
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')
app.config['SESSION_TYPE'] = 'filesystem'

# Create uploads folder if it doesn't exist
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
    image_file.save(image_path)

    # Store image path in session
    session['image_path'] = image_path

    # Analyze the image
    analysis_result = analyze_image(image_path)
    
    # Store the analysis result in session
    try:
        if isinstance(analysis_result, str):
            try:
                analysis_dict = json.loads(analysis_result)
            except json.JSONDecodeError:
                analysis_dict = {"raw_analysis": analysis_result}
        else:
            analysis_dict = analysis_result
            
        session['analysis_result'] = json.dumps(analysis_dict)
    except Exception as e:
        print(f"Error storing analysis in session: {str(e)}")
    
    return jsonify(analysis_result)

@app.route('/query', methods=['POST'])
def query_image():
    data = request.json
    query = data.get('query')
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    # Get the image path from session
    image_path = session.get('image_path')
    
    if not image_path or not os.path.exists(image_path):
        return jsonify({'error': 'No image available. Please upload an image first.'}), 400
    
    # Try using stored analysis if available
    analysis_result = None
    if 'analysis_result' in session:
        try:
            analysis_result = json.loads(session['analysis_result'])
        except Exception as e:
            print(f"Error loading analysis from session: {str(e)}")
    
    # If we have analysis results, try to use them
    if analysis_result:
        query_processor = QueryProcessor(analysis_result)
        try:
            structured_response = query_processor.get_structured_response(query)
            if structured_response and structured_response != {}:
                return jsonify(structured_response)
        except Exception as e:
            print(f"Error in structured query processing: {str(e)}")
    
    # If structured approach doesn't work, use direct image query
    try:
        direct_response = direct_image_query(image_path, query)
        return jsonify({"answer": direct_response})
    except Exception as e:
        print(f"Error in direct image query: {str(e)}")
        return jsonify({"error": "Failed to process your query. Please try again later."})

# Add a route to debug the session
@app.route('/debug_session')
def debug_session():
    if 'analysis_result' in session:
        try:
            analysis = json.loads(session['analysis_result'])
            return jsonify({
                'session_contains_analysis': True,
                'analysis_keys': list(analysis.keys()) if isinstance(analysis, dict) else None,
                'yolo_detections': analysis.get('yolo_detections', []) if isinstance(analysis, dict) else None
            })
        except Exception as e:
            return jsonify({'error': str(e), 'session_contains_analysis': True})
    else:
        return jsonify({'session_contains_analysis': False})

if __name__ == '__main__':
    app.run(debug=True)