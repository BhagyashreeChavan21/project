from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import cv2
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists('uploads'):
    os.makedirs('uploads')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return 'No image part in the form'
    file = request.files['image']
    if file.filename == '':
        return 'No selected file'
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Canny edge detection
    img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    edges = cv2.Canny(img, 100, 200)
    result_path = os.path.join(app.config['UPLOAD_FOLDER'], 'edge_' + filename)
    cv2.imwrite(result_path, edges)

    return render_template('result.html', original=filename, result='edge_' + filename)

if __name__ == '__main__':
    app.run(debug=True)
