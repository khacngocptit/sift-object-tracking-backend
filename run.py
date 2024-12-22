from app import create_app
from flask_cors import CORS
import os
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'

app = create_app()
CORS(app)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

if __name__ == '__main__':
    app.run(debug=True)