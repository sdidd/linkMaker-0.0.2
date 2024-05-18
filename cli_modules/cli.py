import os
import sys
import time
import argparse
from flask import Flask, send_from_directory, abort
from werkzeug.utils import secure_filename
from pyngrok import ngrok

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    filename = secure_filename(filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    else:
        abort(404)

def create_temp_link(file_path):
    filename = secure_filename(os.path.basename(file_path))
    destination = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.rename(file_path, destination)

    # Start ngrok tunnel
    public_url = ngrok.connect(5000)
    print(f" * ngrok tunnel \"{public_url}\" -> \"http://127.0.0.1:5000\"")

    return f"{public_url}/download/{filename}"

def main():
    parser = argparse.ArgumentParser(description='Create a temporary download link for a file.')
    parser.add_argument('file', type=str, help='Path to the file')
    args = parser.parse_args()

    file_path = args.file

    if not os.path.isfile(file_path):
        print("File does not exist.")
        sys.exit(1)

    # Create a temporary download link
    link = create_temp_link(file_path)
    print(f"Temporary download link: {link}")

    # Run Flask app
    app.run(port=5000)

if __name__ == '__main__':
    main()
