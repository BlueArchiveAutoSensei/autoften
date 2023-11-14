import cv2
from ultralytics import YOLO
import time

# Load the YOLOv8 model
model = YOLO(
    r"assets\weights\train32.pt")

# Open the video file
video_path = r"C:\Users\Vickko\Documents\MuMu共享文件夹\VideoRecords\ブルアカ(17).mp4"
cap = cv2.VideoCapture(video_path)

start_time = None
# Loop through the video frames
while cap.isOpened():
    if start_time == None:
        start_time = time.time()
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 inference on the frame
        results = model(frame, stream=True, verbose=False)

        for r in results:
            # Visualize the results on the frame
            annotated_frame = r.plot()

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break
    frame_rate = 1/(time.time()-start_time)
    start_time = time.time()
    print("detection speed: ", frame_rate, "fps")

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
