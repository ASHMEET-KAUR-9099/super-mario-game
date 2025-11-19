from flask import Flask, request, send_file
import os

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        filename = 'screenshot.png'
        file.save(filename)
        return "File successfully uploaded"
    

@app.route('/')
def index():
    return send_file('screenshot.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(port=5000, debug = True)