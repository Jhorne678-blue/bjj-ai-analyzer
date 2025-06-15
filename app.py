from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os

from analyzer import run_fake_analysis

app = Flask(__name__)
app.secret_key = 'supersecretkey'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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
    file.save(filepath)

    # Run AI analysis (currently mocked with random selections)
    analysis = run_fake_analysis(filename)

    return render_template('result.html', analysis=analysis)

if __name__ == "__main__":
    app.run(debug=True)
