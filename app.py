from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from analyzer import run_fake_analysis

app = Flask(__name__)
app.secret_key = 'supersecretkey'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        flash('Please upload a video file.')
        return redirect(url_for('index'))

    file = request.files['video']
    if file.filename == '':
        flash('No selected file.')
        return redirect(url_for('index'))

    if not allowed_file(file.filename):
        flash('Invalid file type.')
        return redirect(url_for('index'))

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        file.save(filepath)
    except Exception as e:
        flash(f"Error saving file: {str(e)}")
        return redirect(url_for('index'))

    try:
        analysis = run_fake_analysis(filename)
    except Exception as e:
        flash(f"Error during analysis: {str(e)}")
        return redirect(url_for('index'))

    return render_template('result.html', analysis=analysis)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
