from flask import Flask, request, render_template_string, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'  # Directory to store uploaded images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
USERNAME = 'admin'  # Change this to your desired username
PASSWORD = 'superbug'  # Change this to a strong password
app.secret_key = 'supersecretkey'  # For flash messages
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Basic authentication
def check_auth(username, password):
    return username == USERNAME and password == PASSWORD

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_auth(username, password):
            return redirect(url_for('upload_file'))
        else:
            flash('Invalid credentials. Please try again.')
    return render_template_string('''
        <!doctype html>
        <title>Login</title>
        <h1>Login</h1>
        <form method="post">
            <label for="username">Username:</label>
            <input type="text" name="username" id="username" required>
            <br>
            <label for="password">Password:</label>
            <input type="password" name="password" id="password" required>
            <br>
            <button type="submit">Login</button>
        </form>
    ''')

# Upload page
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an empty file
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            return redirect(request.url)
    return render_template_string('''
        <!doctype html>
        <title>Upload Image</title>
        <h1>Upload Image</h1>
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <button type="submit">Upload</button>
        </form>
        <p><a href="/login">Logout</a></p>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
