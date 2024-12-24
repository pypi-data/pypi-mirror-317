import json
import math
import os
import shutil

import cv2
import mediapipe as mp
from screeninfo import get_monitors

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 640
CALIBRATION_GRID = [(x / 4, y / 4) for y in range(5) for x in range(5)]
CENTER_POINT = (0.5, 0.5)
MIN_DISTANCE = 50
MAX_DISTANCE = 70
SAMPLES_PER_DOT = 10
WINDOW_NAME = "Eye Tracking"
DATASET_DIR = "output"
SCREEN_DETAILS_FILE = os.path.join(DATASET_DIR, "screen_details.json")
DATASET_FILE = os.path.join(DATASET_DIR, "dataset.json")
IMAGE_FILENAME_FORMAT = os.path.join(
    DATASET_DIR, "frame_{dot_idx}_sample_{sample_idx}.jpg"
)
SHOW_FACE_MESH = True
SHOW_GUIDELINES = True
ZIP_OUTPUT = True
CLEAN = True

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


class DistanceEstimator:
    def __init__(self, focal_length=650, real_face_width=14.0):
        self.focal_length = focal_length
        self.real_face_width = real_face_width

    def calculate_pixel_distance(self, landmark1, landmark2, image_width, image_height):
        x1, y1 = int(landmark1.x * image_width), int(landmark1.y * image_height)
        x2, y2 = int(landmark2.x * image_width), int(landmark2.y * image_height)
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def estimate_distance_from_camera(self, pixel_face_width):
        if pixel_face_width == 0:
            return None
        return (self.real_face_width * self.focal_length) / pixel_face_width


class EyeTracker:
    def __init__(self, max_faces=1, detection_confidence=0.5, tracking_confidence=0.5):
        self.face_mesh = mp_face_mesh.FaceMesh(
            max_num_faces=max_faces,
            refine_landmarks=True,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence,
        )

    def process_frame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return self.face_mesh.process(rgb_frame)

    def draw_landmarks(self, frame, face_landmarks):
        mp_drawing.draw_landmarks(
            image=frame,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style(),
        )

    def save_landmarks_image(self, frame, filepath):
        cv2.imwrite(filepath, frame)


def set_window_center(window_name):
    monitor = get_monitors()[0]
    screen_width = monitor.width
    screen_height = monitor.height
    x = (screen_width - WINDOW_WIDTH) // 2
    y = (screen_height - WINDOW_HEIGHT) // 2
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, WINDOW_WIDTH, WINDOW_HEIGHT)
    cv2.moveWindow(window_name, x, y)


def draw_guidelines(frame):
    height, width, _ = frame.shape
    cv2.line(frame, (width // 2, 0), (width // 2, height), (0, 255, 255), 2)
    cv2.line(
        frame, (0, int(height * 1 / 3)), (width, int(height * 1 / 3)), (255, 255, 0), 2
    )


def check_head_position(landmarks, image_width, image_height):
    nose_x = int(landmarks[1].x * image_width)
    nose_y = int(landmarks[1].y * image_height)

    middle_x = image_width // 2
    middle_y = image_height // 2

    two_thirds_y = int(image_height * 1 / 3)

    threshold_x = image_width * 0.1  # 10% of the screen width
    threshold_y = image_height * 0.05  # 5% of the screen height

    horizontal_ok = abs(nose_x - middle_x) <= threshold_x
    vertical_ok = (
        abs(nose_y - middle_y) <= threshold_y
        or abs(nose_y - two_thirds_y) <= threshold_y
    )

    return horizontal_ok, vertical_ok


def display_position_warnings(frame, horizontal_ok, vertical_ok):
    if horizontal_ok and vertical_ok:
        cv2.putText(
            frame,
            "Eyes are well aligned!",
            (50, 150),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )
    else:
        if not horizontal_ok:
            cv2.putText(
                frame,
                "Align your eyes horizontally!",
                (50, 150),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2,
            )
        if not vertical_ok:
            cv2.putText(
                frame,
                "Align your eyes vertically!",
                (50, 200),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2,
            )


def display_warning(frame, message):
    cv2.putText(
        frame,
        message,
        (50, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2,
    )


def display_distance(
    frame, distance, min_distance, max_distance, during_collection=False
):
    if distance is not None:
        if during_collection:
            status = (
                "Move back to the good range!"
                if distance < min_distance
                else "Move closer to the monitor!"
            )
        else:
            status = (
                "Good distance"
                if min_distance <= distance <= max_distance
                else "Adjust your distance!"
            )
        color = (0, 255, 0) if min_distance <= distance <= max_distance else (0, 0, 255)
        cv2.putText(
            frame,
            f"Distance: {distance:.2f} cm - {status}",
            (50, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            color,
            2,
        )


def save_screen_details(
    screen_width, screen_height, window_width, window_height, filename
):
    details = {
        "screen_width": screen_width,
        "screen_height": screen_height,
        "window_width": window_width,
        "window_height": window_height,
    }
    with open(filename, "w") as f:
        json.dump(details, f, indent=4)


def check_eye_position(landmarks, image_width, image_height):
    left_eye_x = int((landmarks[33].x + landmarks[133].x) / 2 * image_width)
    left_eye_y = int((landmarks[33].y + landmarks[133].y) / 2 * image_height)
    right_eye_x = int((landmarks[362].x + landmarks[263].x) / 2 * image_width)
    right_eye_y = int((landmarks[362].y + landmarks[263].y) / 2 * image_height)

    eye_midpoint_x = (left_eye_x + right_eye_x) // 2
    eye_midpoint_y = (left_eye_y + right_eye_y) // 2

    middle_x = image_width // 2
    middle_y = image_height // 2

    two_thirds_y = int(image_height * 1 / 3)

    threshold_x = image_width * 0.01  # 1% of the screen width
    threshold_y = image_height * 0.05  # 5% of the screen height

    horizontal_ok = abs(eye_midpoint_x - middle_x) <= threshold_x
    vertical_ok = (
        abs(eye_midpoint_y - middle_y) <= threshold_y
        or abs(eye_midpoint_y - two_thirds_y) <= threshold_y
    )

    return horizontal_ok, vertical_ok


def collect_data():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Camera not accessible.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WINDOW_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, WINDOW_HEIGHT)
    tracker = EyeTracker()
    estimator = DistanceEstimator()

    set_window_center(WINDOW_NAME)

    if os.path.exists(DATASET_DIR):
        shutil.rmtree(DATASET_DIR)
    os.makedirs(DATASET_DIR, exist_ok=True)

    monitor = get_monitors()[0]
    save_screen_details(
        monitor.width, monitor.height, WINDOW_WIDTH, WINDOW_HEIGHT, SCREEN_DETAILS_FILE
    )

    dataset = []

    calibration_mode = False
    collecting_samples = False

    while True:
        success, frame = cap.read()
        if not success:
            print("Ignoring empty frame.")
            continue

        display_frame = frame.copy()

        height, width, _ = frame.shape

        if SHOW_GUIDELINES:
            draw_guidelines(display_frame)

        results = tracker.process_frame(frame)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                pixel_face_width = estimator.calculate_pixel_distance(
                    face_landmarks.landmark[33],
                    face_landmarks.landmark[263],
                    width,
                    height,
                )
                distance = estimator.estimate_distance_from_camera(pixel_face_width)

                horizontal_ok, vertical_ok = check_eye_position(
                    face_landmarks.landmark, width, height
                )

                display_position_warnings(display_frame, horizontal_ok, vertical_ok)
                display_distance(display_frame, distance, MIN_DISTANCE, MAX_DISTANCE)

                if SHOW_GUIDELINES:
                    draw_guidelines(display_frame)
                if SHOW_FACE_MESH:
                    tracker.draw_landmarks(display_frame, face_landmarks)
                if collecting_samples and (
                    distance is None
                    or distance < MIN_DISTANCE
                    or distance > MAX_DISTANCE
                    or not (horizontal_ok and vertical_ok)
                ):
                    collecting_samples = False
                    cv2.imshow(WINDOW_NAME, display_frame)
                    cv2.waitKey(100)
                    continue

                if (
                    distance is not None
                    and MIN_DISTANCE <= distance <= MAX_DISTANCE
                    and horizontal_ok
                    and vertical_ok
                ):
                    if not collecting_samples:
                        cv2.putText(
                            display_frame,
                            "Press 'a' to continue calibration",
                            (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (255, 255, 255),
                            2,
                        )

        if calibration_mode:
            for idx, point in enumerate(CALIBRATION_GRID):
                target_x = int(point[0] * width)
                target_y = int(point[1] * height)

                sample_idx = 0
                while sample_idx < SAMPLES_PER_DOT:
                    success, frame = cap.read()
                    if not success:
                        print("Ignoring empty frame during calibration.")
                        continue

                    display_frame = frame.copy()

                    height, width, _ = frame.shape

                    results = tracker.process_frame(frame)
                    if results.multi_face_landmarks:
                        for face_landmarks in results.multi_face_landmarks:
                            pixel_face_width = estimator.calculate_pixel_distance(
                                face_landmarks.landmark[33],
                                face_landmarks.landmark[263],
                                width,
                                height,
                            )
                            distance = estimator.estimate_distance_from_camera(
                                pixel_face_width
                            )

                            horizontal_ok, vertical_ok = check_eye_position(
                                face_landmarks.landmark, width, height
                            )

                            if (
                                distance is None
                                or distance < MIN_DISTANCE
                                or distance > MAX_DISTANCE
                                or not (horizontal_ok and vertical_ok)
                            ):
                                if SHOW_GUIDELINES:
                                    draw_guidelines(display_frame)
                                if SHOW_FACE_MESH:
                                    tracker.draw_landmarks(
                                        display_frame, face_landmarks
                                    )
                                display_distance(
                                    display_frame,
                                    distance,
                                    MIN_DISTANCE,
                                    MAX_DISTANCE,
                                    during_collection=True,
                                )
                                display_position_warnings(
                                    display_frame, horizontal_ok, vertical_ok
                                )
                                cv2.imshow(WINDOW_NAME, display_frame)
                                cv2.waitKey(100)
                                continue

                            cv2.circle(
                                display_frame, (target_x, target_y), 15, (0, 0, 255), -1
                            )
                            cv2.putText(
                                display_frame,
                                f"Dot {idx + 1}/{len(CALIBRATION_GRID)}, Sample {sample_idx + 1}/{SAMPLES_PER_DOT}",
                                (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1,
                                (255, 255, 255),
                                2,
                            )

                            image_filepath = IMAGE_FILENAME_FORMAT.format(
                                dot_idx=idx, sample_idx=sample_idx
                            )
                            tracker.save_landmarks_image(frame, image_filepath)

                            all_landmarks = [
                                {"x": lm.x * width, "y": lm.y * height}
                                for lm in face_landmarks.landmark
                            ]
                            dataset.append(
                                {
                                    "image_path": image_filepath,
                                    "dot_x": target_x,
                                    "dot_y": target_y,
                                    "distance": distance,
                                    "eye_landmarks": all_landmarks,
                                }
                            )
                            sample_idx += 1

                    cv2.imshow(WINDOW_NAME, display_frame)
                    key = cv2.waitKey(10)
                    if key == 27:
                        calibration_mode = False
                        collecting_samples = False
                        break

            calibration_mode = False

        cv2.imshow(WINDOW_NAME, display_frame)
        key = cv2.waitKey(1)
        if key == 27:
            break
        if key == ord("a"):
            calibration_mode = True
            collecting_samples = True

    cap.release()
    cv2.destroyAllWindows()

    with open(DATASET_FILE, "w") as f:
        json.dump(dataset, f, indent=4)

    if ZIP_OUTPUT:
        if os.path.exists(f"{DATASET_DIR}.zip"):
            os.remove(f"{DATASET_DIR}.zip")
        shutil.make_archive(DATASET_DIR, "zip", DATASET_DIR)
    if CLEAN:
        shutil.rmtree(DATASET_DIR)
