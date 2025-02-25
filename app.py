import os
import zipfile
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

UPLOAD_FOLDER = "tof"
ZIP_FILE = "tof.zip"

# Assurer que le dossier existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Décompression si le zip existe
if os.path.exists(ZIP_FILE):
    with zipfile.ZipFile(ZIP_FILE, 'r') as zip_ref:
        zip_ref.extractall(UPLOAD_FOLDER)

@app.route("/")
def gallery():
    images = [f for f in os.listdir(UPLOAD_FOLDER) if f.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'webp'))]
    return render_template("gallery.html", images=images)

@app.route("/tof/<path:filename>")
def serve_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
