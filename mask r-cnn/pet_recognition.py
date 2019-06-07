import numpy as np
import cv2
import mrcnn.config
import mrcnn.utils
from mrcnn.model import MaskRCNN
from pathlib import Path
import os


class MaskRCNNConfig(mrcnn.config.Config):
    NAME = "coco_pretrained_model_config"
    IMAGES_PER_GPU = 1
    GPU_COUNT = 1
    NUM_CLASSES = 1 + 80  # COCO's dataset have 80 classes + 1 hidden class
    DETECTION_MIN_CONFIDENCE = 0.6


# filtering result list. Need only cat
def get_cat_boxes(boxes, class_ids):
    cat_boxes = []
    for i, box in enumerate(boxes):
        if class_ids[i] in [16]:
            cat_boxes.append(box)

    return np.array(cat_boxes)


ROOT_DIR = Path(".")
# save log
MODEL_DIR = os.path.join(ROOT_DIR,"logs")

COCO_MODEL_PATH = os.path.join(ROOT_DIR,"mask_rcnn_coco.h5")

# download COCO's dataset
if not os.path.exists(COCO_MODEL_PATH):
    mrcnn.utils.download_trained_weights(COCO_MODEL_PATH)

IMAGE_DIR = os.path.join(ROOT_DIR,"images")

VIDEO_SOURCE = os.path.join("test_images","Awesome Funny Pet Animals\' Life.mp4")

# create model
model = MaskRCNN(mode='inference', model_dir=MODEL_DIR, config=MaskRCNNConfig())

# load model
model.load_weights(COCO_MODEL_PATH, by_name=True)

detected_cat_boxes = None

# download video file
video_capture = cv2.VideoCapture(VIDEO_SOURCE)

free_space_frames = 0

while video_capture.isOpened():
    success, frame = video_capture.read()
    if not success:
        break

    # convert to BGR
    rgb_image = frame[:, :, ::-1]

    results = model.detect([rgb_image], verbose=0)
    r = results[0]

    if detected_cat_boxes is None or len(detected_cat_boxes) == 0:
        # print('first frame')
        detected_cat_boxes = get_cat_boxes(r['rois'], r['class_ids'])
    else:
        cat_boxes = get_cat_boxes(r['rois'], r['class_ids'])
        
        # print(len(detected_cat_boxes), ' - detected_cat_boxes')
        # print(len(cat_boxes), ' - cat_boxes')
        
        if len(detected_cat_boxes) == 0 or len(cat_boxes) == 0:
            print("Cats not found in frame of video!")
        else:
            print("Cats found in frame of video:")
            for box in cat_boxes:
                print("Cat: ", box)
                y1,x1,y2,x2 = box
                cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0),1)

            overlaps = mrcnn.utils.compute_overlaps(detected_cat_boxes, cat_boxes)

            free_space = False

            for detected_area,  overlap_areas in zip(detected_cat_boxes, overlaps):
                max_IoU_overlap = np.max(overlap_areas)
                y1,x1, y2, x2 = detected_area
                if max_IoU_overlap < 0.15:
                    free_space = True
            
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, f"{max_IoU_overlap:0.2}", (x1 + 6, y1 - 6), font, 0.3, (255,255,255))

            print(free_space, ' - free_space')
            if free_space:
                free_space_frames += 1
            else:
                free_space_frames = 0
            
            print('free_space_frames - ', free_space_frames)
            if free_space_frames > 10:
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, f"SPACE AVAILABLE!", (10, 150), font, 3.0, (0, 255, 0), 2, cv2.FILLED)
    
    cv2.imshow("Video", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
