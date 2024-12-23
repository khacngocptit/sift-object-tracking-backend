from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
import cv2

# Import hàm track_object_with_roi từ file chính của bạn
from utils import track_object_with_roi

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

@app.route('/upload', methods=['POST'])
def upload_files():
    # Kiểm tra nếu không có file nào được upload
    
    if 'video' not in request.files or 'roi' not in request.files:
        return jsonify({'error': 'Video and ROI files are required.'}), 400

    video_file = request.files['video']
    roi_file = request.files['roi']

    if video_file.filename == '' or roi_file.filename == '':
        return jsonify({'error': 'Empty file(s) provided.'}), 400

    # Lưu các file đã upload
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(video_file.filename))
    roi_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(roi_file.filename))

    video_file.save(video_path)
    roi_file.save(roi_path)

    try:
        # Gọi hàm track_object_with_roi
        output_video_path = track_object_with_roi(video_path, roi_path, output_dir=app.config['OUTPUT_FOLDER'])
        return jsonify({'message': 'Processing complete.', 'output_video': output_video_path}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)