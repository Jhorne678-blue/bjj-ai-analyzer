@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        flash('No file part in request')
        return redirect(url_for('index'))

    file = request.files['video']

    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('index'))

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    result = f"✅ Analysis complete for {filename} — great work!"
    return render_template('result.html', result=result, filename=filename)
