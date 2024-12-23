import cv2
import numpy as np
import os
def track_object_with_roi(video_path, roi_path, output_dir="output", frame_skip=2):
    """
    Tracks an object in a video using SIFT features, based on the provided ROI image.

    Args:
        video_path (str): Path to the input video.
        roi_path (str): Path to the saved ROI image.
        output_dir (str): Directory to save the output video.
        frame_skip (int): Number of frames to skip during processing for faster performance.

    Returns:
        output_video_path (str): Path to the saved output video.
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Initialize SIFT and FLANN matcher
    sift = cv2.SIFT_create(contrastThreshold=0.04, edgeThreshold=10)
    index_params = dict(algorithm=1, trees=5)  # KD-Tree
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    # Load ROI image and compute SIFT features
    roi = cv2.imread(roi_path)
    if roi is None:
        raise FileNotFoundError(f"ROI image not found at {roi_path}")

    keypoints1, descriptors1 = sift.detectAndCompute(roi, None)
    if descriptors1 is None:
        raise ValueError("No SIFT features detected in the ROI image.")

    # Open the video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open video at {video_path}")

    # Setup video writer
    frame_height, frame_width = (360, 640)  # Resize dimensions
    output_video_path = os.path.join(output_dir, "output_video.avi")
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(output_video_path, fourcc, 20.0, (frame_width, frame_height))
    print(f"Output video will be saved to {output_video_path}")

    while True:
        # Skip frames for faster processing
        for _ in range(frame_skip - 1):
            cap.grab()

        ret, frame = cap.read()
        if not ret:
            break
        # Resize frame for processing
        frame = cv2.resize(frame, (640, 360))
        keypoints2, descriptors2 = sift.detectAndCompute(frame, None)

        if descriptors1 is not None and descriptors2 is not None:
            matches = flann.knnMatch(descriptors1, descriptors2, k=2)

            # Lowe's ratio test
            good_matches = []
            for m, n in matches:
                if m.distance < 0.7 * n.distance:
                    good_matches.append(m)

            # Perform homography and draw bounding box
            if len(good_matches) > 10:
                src_pts = np.float32(
                    [keypoints1[m.queryIdx].pt for m in good_matches]
                ).reshape(-1, 1, 2)
                dst_pts = np.float32(
                    [keypoints2[m.trainIdx].pt for m in good_matches]
                ).reshape(-1, 1, 2)

                # Compute homography
                M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
                if M is not None:
                    h, w = roi.shape[:2]
                    pts = np.float32([[0, 0], [0, h], [w, h], [w, 0]]).reshape(-1, 1, 2)
                    dst = cv2.perspectiveTransform(pts, M)

                    # Draw bounding box on the frame
                    frame = cv2.polylines(
                        frame, [np.int32(dst)], True, (0, 255, 0), 2, cv2.LINE_AA
                    )

        # Write processed frame to the output video
        out.write(frame)

        # Display the frame (optional, press 'q' to quit)
        cv2.imshow("Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Video saved to {output_video_path}")

    return output_video_path