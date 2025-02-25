import os
import zipfile
import urllib.parse
import stat
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

UPLOAD_FOLDER = "tof"
ZIP_FILE = "tof.zip"

# Assurer que le dossier existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Décompression du zip si nécessaire
if os.path.exists(ZIP_FILE):
    with zipfile.ZipFile(ZIP_FILE, 'r') as zip_ref:
        zip_ref.extractall(UPLOAD_FOLDER)

    # Assurer que les fichiers extraits sont lisibles
    for file in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, file)
        os.chmod(file_path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)  # Donne les bonnes permissions

@app.route("/")
def gallery():
    # Liste les images et encode les noms pour éviter les problèmes d'URL
    images = [urllib.parse.quote(f) for f in os.listdir(UPLOAD_FOLDER) 
              if f.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp', 'svg'))]
    return render_template("gallery.html", images=images)

@app.route("/tof/<path:filename>")
def serve_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# Endpoint pour voir quels fichiers sont réellement sur le serveur
@app.route("/debug")
def debug():
    files = os.listdir(UPLOAD_FOLDER)
    return "<br>".join(files)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
