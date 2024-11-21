import os
import zipfile
import hashlib
import random
import string
import shutil
import logging
import sys
import time
from flask import Flask, render_template, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename
from subtitle_toastifier import process_srt_file

# Ensure logs folder exists
log_dir = './logs'
os.makedirs(log_dir, exist_ok=True)

# Set up logging to rotate daily
def get_log_filename():
    timestamp = time.strftime("%Y-%m-%d")
    return os.path.join(log_dir, f"{timestamp}_toastifier.log")

log_file = get_log_filename()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

# Redirect stdout and stderr to log file
sys.stdout = open(log_file, "a")
sys.stderr = open(log_file, "a")

# Function to check and create a new log file every day
def rotate_log_file():
    global log_file
    new_log_file = get_log_filename()
    if log_file != new_log_file:
        log_file = new_log_file
        logging.handlers[0].close()
        logging.handlers[0] = logging.FileHandler(log_file)

# Create new log file every day at midnight
def daily_log_rotation():
    while True:
        time.sleep(60)
        rotate_log_file()

# Start log rotation in a separate thread
import threading
log_thread = threading.Thread(target=daily_log_rotation, daemon=True)
log_thread.start()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/app/uploads'
app.config['PROCESSED_FOLDER'] = '/app/processed'
app.config['ARCHIVE_FOLDER'] = '/app/processed_archive'

# Create folders if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)
os.makedirs(app.config['ARCHIVE_FOLDER'], exist_ok=True)

def generate_unique_filename(filename):
    """
    Generates a unique filename by appending an MD5 hash to the original filename.
    """
    salt = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    unique_id = hashlib.md5((filename + salt).encode()).hexdigest()
    name, ext = os.path.splitext(filename)
    return f"{name}_{unique_id}{ext}"

@app.route('/')
def index():
    logging.info("Accessed index page.")
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    logging.info("Received file upload request.")
    # Clear processed folder for fresh upload
    for f in os.listdir(app.config['PROCESSED_FOLDER']):
        os.remove(os.path.join(app.config['PROCESSED_FOLDER'], f))

    files = request.files.getlist('files[]')
    processed_files = []
    
    for file in files:
        if file.filename.endswith('.srt'):
            logging.info(f"Processing file: {file.filename}")
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            if "_processed.srt" in filename:
                filename = generate_unique_filename(filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Process the file
            process_srt_file(file_path)
            
            processed_file_path = file_path.replace('.srt', '_processed.srt')
            unique_filename = generate_unique_filename(os.path.basename(processed_file_path))
            final_path = os.path.join(app.config['ARCHIVE_FOLDER'], unique_filename)
            shutil.move(processed_file_path, final_path)
            processed_files.append(final_path)

    if len(processed_files) == 1:
        return send_file(processed_files[0], as_attachment=True)
    else:
        zip_name = 'processed_files.zip'
        zip_path = os.path.join(app.config['PROCESSED_FOLDER'], zip_name)
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file_path in processed_files:
                zipf.write(file_path, os.path.basename(file_path))

        archived_zip_path = os.path.join(app.config['ARCHIVE_FOLDER'], zip_name)
        shutil.move(zip_path, archived_zip_path)

        return send_file(archived_zip_path, as_attachment=True)

if __name__ == "__main__":
    logging.info("Starting Flask application.")
    app.run(host="0.0.0.0", port=5000)
