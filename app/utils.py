import cv2
import os

# Lấy đường dẫn tuyệt đối đến thư mục `app`
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_FOLDER = os.path.join(BASE_DIR, 'processed')

# Đảm bảo thư mục `processed` tồn tại
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def process_image(image_path):
    object_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    sift = cv2.SIFT_create()
    keypoints, _ = sift.detectAndCompute(object_image, None)
    output_image = cv2.drawKeypoints(object_image, keypoints, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    processed_path = os.path.join(PROCESSED_FOLDER, 'processed_image.jpg')
    cv2.imwrite(processed_path, output_image)
    return processed_path

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    processed_path = os.path.join(PROCESSED_FOLDER, 'processed_video.avi')
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(processed_path, fourcc, fps, (width, height))

    sift = cv2.SIFT_create()
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        keypoints, _ = sift.detectAndCompute(gray_frame, None)
        output_frame = cv2.drawKeypoints(frame, keypoints, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        out.write(output_frame)

    cap.release()
    out.release()
    return processed_path
