from IPython import display
display.clear_output()

import ultralytics
ultralytics.checks()

from IPython import display
display.clear_output()

import supervision as sv
print("supervision.__version__:", sv.__version__)

MODEL = "yolov8n.pt"

import supervision as sv
import numpy as np

from ultralytics import YOLO

model = YOLO(MODEL)
model.fuse()

# dict maping class_id to class_name
CLASS_NAMES_DICT = model.model.names

# class_ids of interest - car, motorcycle, bus and truck
selected_classes = [2, 3, 5, 7]
selected_classes = [0]

print(model.model.names)

SOURCE_VIDEO_PATH = r'C:\Users\eitan\Pictures\comercio_ambulante_2_corte2.mp4'
TARGET_VIDEO_PATH = r'C:\Users\eitan\Pictures\resultado.mp4'

# create VideoInfo instance
video_info = sv.VideoInfo.from_video_path(SOURCE_VIDEO_PATH)

# create BYTETracker instance
byte_tracker = sv.ByteTrack(track_thresh=0.15, track_buffer=video_info.fps * 2, match_thresh=0.8, frame_rate=video_info.fps)

# create frame generator
generator = sv.get_video_frames_generator(SOURCE_VIDEO_PATH)

box_annotator = sv.BoxAnnotator(color=sv.Color(r=0, g=102, b=0), text_color=sv.Color.white(), thickness=1, text_thickness=1, text_scale=0.5)

def callback(frame: np.ndarray, index:int) -> np.ndarray:
    # model prediction on single frame and conversion to supervision Detections
    results = model(frame, verbose=False)[0]
    detections = sv.Detections.from_ultralytics(results)
    # only consider class id from selected_classes define above
    detections = detections[np.isin(detections.class_id, selected_classes)]
    # tracking detections
    detections = byte_tracker.update_with_detections(detections)

    labels = []
    for bbox, _, confidence, class_id, tracker_id in detections:
        labels.append(f"{[tracker_id]}")

    annotated_frame = frame.copy()

    annotated_frame=box_annotator.annotate(
        scene=annotated_frame,
        detections=detections,
        labels=labels
        )
    return  annotated_frame

# process the whole video
sv.process_video(
    source_path = SOURCE_VIDEO_PATH,
    target_path = TARGET_VIDEO_PATH,
    callback=callback
)

import cv2
print(cv2.__version__)

video = cv2.VideoCapture(TARGET_VIDEO_PATH)

while True:
    ret, frame = video.read()
    if not ret:
        break
    cv2.imshow('Video', frame)

    if cv2.waitKey(video_info.fps) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()