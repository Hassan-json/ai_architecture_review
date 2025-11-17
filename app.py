import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from config import Config
from services.ai_reviewer import ArchitectureReviewer

app = Flask(__name__)
app.config.from_object(Config)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize AI reviewer lazily (only when needed)
reviewer = None


def get_reviewer():
    """Get or initialize the AI reviewer"""
    global reviewer
    if reviewer is None:
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set. Please add it to your .env file")
        reviewer = ArchitectureReviewer()
    return reviewer


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    """Render the main web UI page"""
    return render_template('index.html')


@app.route('/api/review', methods=['POST'])
def review_architecture():
    """
    API endpoint to review architecture diagram
    Accepts: multipart/form-data with 'image' file
    Returns: JSON with review results
    """
    # Check if file is in request
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'No image file provided'}), 400

    file = request.files['image']

    # Check if file is selected
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400

    # Check if file type is allowed
    if not allowed_file(file.filename):
        return jsonify({
            'success': False,
            'error': f'Invalid file type. Allowed types: {", ".join(app.config["ALLOWED_EXTENSIONS"])}'
        }), 400

    try:
        # Save the file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Review the architecture
        result = get_reviewer().review_architecture(filepath)

        # Optionally delete the file after review (for privacy/storage)
        # os.remove(filepath)

        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    # Check if OpenAI API key is set
    if not Config.OPENAI_API_KEY:
        print("\n" + "="*60)
        print("WARNING: OPENAI_API_KEY is not set!")
        print("="*60)
        print("\nTo use this app, you need to:")
        print("1. Get an API key from: https://platform.openai.com/api-keys")
        print("2. Edit the .env file and add your key:")
        print("   OPENAI_API_KEY=sk-proj-your-key-here")
        print("\nThe app will start, but reviews won't work until you add the key.")
        print("="*60 + "\n")
    else:
        print(f"\n✓ OpenAI API configured (using model: {Config.OPENAI_MODEL})")
        print(f"✓ Server starting...\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
