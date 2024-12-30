import os
import datetime
from ultralytics import YOLO
import time
from src.Utilities import log
import cv2
import argparse
import supervision as sv
from src.Utilities import flexMenu


def create_directories(path: str):
    """Create directories if they don't exist."""
    if not os.path.exists(path):
        os.makedirs(path)
        log.logger.info(f"Created missing directory: {path}")


def create_video_writer(video_cap, output_filename):
    """Initialize a video writer object."""
    frame_width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(video_cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    return cv2.VideoWriter(output_filename, fourcc, fps, (frame_width, frame_height))


def stream():
    current_time = datetime.datetime.now()
    desired_format = "%Y-%m-%d_%H-%M-%S_"
    formatted_time = current_time.strftime(desired_format)

    log.logger.info("\nSTREAM START")
    start_time = time.time()

    def parse_arguments() -> argparse.Namespace:
        parser = argparse.ArgumentParser(description="YOLOv8 live")
        parser.add_argument("--webcam-resolution", default=[1920, 1080], nargs=2, type=int)
        return parser.parse_args()

    try:
        # Define the base output path
        base_path = "./OUTPUT/runs/Streams"
        create_directories(base_path)

        model_path = "./OUTPUT/Train/"
        x = os.listdir(model_path)
        train = flexMenu.display_options(x)
        model_path = model_path + train + "/weights/"
        x = os.listdir(model_path)
        m = flexMenu.display_options(x)
        model_path = model_path + "/" + m
        m = m.rsplit(".", 1)[0]

        model = YOLO(model_path)
        args = parse_arguments()
        frame_width, frame_height = args.webcam_resolution
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

        output_file = os.path.join(base_path, f"{formatted_time}{train}{m}.mp4")
        writer = create_video_writer(cap, output_file)

        box_annotator = sv.BoxAnnotator(thickness=2)

        while True:
            ret, frame = cap.read()
            results = model(frame)
            detections = sv.Detections.from_ultralytics(results[0])
            frame = box_annotator.annotate(scene=frame, detections=detections)

            if not detections.class_id.any() == 0:
                print('ALAAAAAAARRM RINGING FIRE !!!!!')

            cv2.imshow("yolov8", frame)
            writer.write(frame)

            if cv2.waitKey(30) == 27:  # ESC key to exit
                break

        cap.release()
        writer.release()
        cv2.destroyAllWindows()

    except Exception as e:
        end_time = time.time()
        log.logger.error(f"\nAn error occurred: {e}\nExecution time: %.2f seconds", end_time - start_time)
    else:
        end_time = time.time()
        log.logger.info("\nNo errors occurred DONE SUCCESS\nExecution time: %.2f seconds", end_time - start_time)
    finally:
        log.logger.critical("\nSTREAM EXIT")
        print("\n")
