from flask import Blueprint, request, send_file, current_app
from .utils import process_image, process_video
import os

bp = Blueprint('routes', __name__)

@bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return {'error': 'No file provided'}, 400

    file = request.files['file']
    if file.filename == '':
        return {'error': 'No file selected'}, 400

    upload_folder = current_app.config['UPLOAD_FOLDER']
    file_path = os.path.join(upload_folder, file.filename)
    file.save(file_path)

    if file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        processed_path = process_image(file_path)
        return send_file(processed_path, mimetype='image/jpeg')
    elif file.filename.lower().endswith(('.mp4', '.avi', '.mov')):
        processed_path = process_video(file_path)
        return send_file(processed_path, mimetype='video/avi')
    else:
        return {'error': 'Unsupported file format'}, 400
