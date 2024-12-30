import json
import math
import os
import shutil
import time
from typing import Tuple

import cv2
import mediapipe as mp
from screeninfo import get_monitors

# Mediapipe configurations
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

    def estimate_distance(self, pixel_face_width):
        return (
            (self.real_face_width * self.focal_length) / pixel_face_width
            if pixel_face_width
            else None
        )


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
            connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style(),
        )


class MessageService:
    @staticmethod
    def display_feedback(
        frame, horizontal_ok, vertical_ok, distance_ok, distance, debug_mode
    ):
        if debug_mode or not (horizontal_ok and vertical_ok and distance_ok):
            height, width, _ = frame.shape
            if not horizontal_ok:
                MessageService.display_message(
                    frame,
                    "Align nose horizontally",
                    (width - 500, height - 50),
                    (0, 0, 255),
                )
            if not vertical_ok:
                MessageService.display_message(
                    frame,
                    "Align eyes vertically",
                    (width - 500, height - 100),
                    (0, 0, 255),
                )
            if distance is not None:
                color = (0, 255, 0) if distance_ok else (0, 0, 255)
                MessageService.display_message(
                    frame,
                    f"Correct Distance: {distance:.2f} cm",
                    (width - 500, height - 150),
                    color,
                )

    @staticmethod
    def display_message(
        frame, message, position: Tuple[float, float], color=(0, 255, 0)
    ):
        cv2.putText(
            frame,
            message,
            position,
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            color,
            2,
        )


class HeadController:
    def __init__(
        self,
        distance_estimator,
        width_threshold=0.1,
        height_threshold=0.05,
        min_distance=50,
        max_distance=70,
    ):
        self.distance_estimator = distance_estimator
        self.width_threshold = width_threshold
        self.height_threshold = height_threshold
        self.min_distance = min_distance
        self.max_distance = max_distance

    def is_head_position_valid(self, landmarks, image_width, image_height):
        left_eye_y = int((landmarks[159].y + landmarks[145].y) / 2 * image_height)
        right_eye_y = int((landmarks[386].y + landmarks[374].y) / 2 * image_height)
        nose_x = int(landmarks[1].x * image_width)

        middle_x = image_width // 2
        two_thirds_y = int(image_height * 1 / 3)

        threshold_x = image_width * self.width_threshold
        threshold_y = image_height * self.height_threshold

        horizontal_ok = abs(nose_x - middle_x) <= threshold_x
        vertical_ok = (
            abs(left_eye_y - two_thirds_y) <= threshold_y
            and abs(right_eye_y - two_thirds_y) <= threshold_y
        )

        return horizontal_ok, vertical_ok

    def is_distance_valid(self, pixel_face_width):
        if not pixel_face_width:
            return False, None

        distance = self.distance_estimator.estimate_distance(pixel_face_width)
        return self.min_distance <= distance <= self.max_distance, distance


# Helper functions
def initialize_output_directory(dataset_dir):
    if os.path.exists(dataset_dir):
        shutil.rmtree(dataset_dir)
    os.makedirs(dataset_dir, exist_ok=True)


def save_screen_details(screen_details_file, window_width, window_height):
    monitor = get_monitors()[0]
    details = {
        "screen_width": monitor.width,
        "screen_height": monitor.height,
        "window_width": window_width,
        "window_height": window_height,
        "monitors": str(get_monitors()),
    }
    with open(screen_details_file, "w") as f:
        json.dump(details, f, indent=4)


def draw_guidelines(frame):
    height, width, _ = frame.shape
    cv2.line(frame, (width // 2, 0), (width // 2, height), (0, 255, 255), 2)
    cv2.line(frame, (0, height // 3), (width, height // 3), (255, 255, 0), 2)


def draw_dot(frame, point, frame_width, frame_height):
    x = int(point[0] * frame_width)
    y = int(point[1] * frame_height)
    cv2.circle(frame, (x, y), 10, (0, 0, 255), -1)


def apply_gray_overlay(frame):
    gray_screen = frame.copy()
    gray_screen[:, :, :] = 255 * 0.18
    return gray_screen


def start_collection(
    window_width,
    window_height,
    calibration_grids,
    min_distance,
    max_distance,
    samples_per_dot,
    window_name,
    dataset_dir,
    screen_details_file,
    dataset_file,
    image_filename_format,
    zip_output,
    clean,
    debug_mode,
):
    initialize_output_directory(dataset_dir)
    save_screen_details(screen_details_file, window_width, window_height)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Camera not accessible.")
        return
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    time.sleep(0.1)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, window_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, window_height)

    tracker = EyeTracker()
    estimator = DistanceEstimator()
    head_controller = HeadController(
        estimator, min_distance=min_distance, max_distance=max_distance
    )

    dataset = {"3x3": [], "5x5": []}

    for grid_label, calibration_grid in calibration_grids.items():
        adjust_mode = False
        while True:
            success, frame = cap.read()
            if not success:
                print("Ignoring empty frame.")
                continue

            display_frame = frame.copy()
            MessageService.display_message(
                display_frame,
                f"Press 'a' to start {grid_label} grid calibration",
                (50, 50),
            )
            cv2.imshow(window_name, display_frame)

            if cv2.waitKey(1) == ord("a"):
                break

        for point in calibration_grid:
            sample_count = 0
            while sample_count < samples_per_dot:
                success, frame = cap.read()
                if not success:
                    print("Ignoring empty frame.")
                    continue

                clear_frame = frame.copy()
                display_frame = frame.copy()
                results = tracker.process_frame(frame)

                if results.multi_face_landmarks:
                    horizontal_ok, vertical_ok, distance_ok = True, True, True
                    for face_landmarks in results.multi_face_landmarks:
                        pixel_face_width = estimator.calculate_pixel_distance(
                            face_landmarks.landmark[33],
                            face_landmarks.landmark[263],
                            frame.shape[1],
                            frame.shape[0],
                        )

                        horizontal_ok, vertical_ok = (
                            head_controller.is_head_position_valid(
                                face_landmarks.landmark,
                                frame.shape[1],
                                frame.shape[0],
                            )
                        )

                        distance_ok, _ = head_controller.is_distance_valid(
                            pixel_face_width
                        )

                    if not (horizontal_ok and vertical_ok and distance_ok):
                        draw_guidelines(display_frame)
                        tracker.draw_landmarks(
                            display_frame, results.multi_face_landmarks[0]
                        )
                        adjust_mode = True

                draw_dot(display_frame, point, frame.shape[1], frame.shape[0])

                if results.multi_face_landmarks:
                    for face_landmarks in results.multi_face_landmarks:
                        pixel_face_width = estimator.calculate_pixel_distance(
                            face_landmarks.landmark[33],
                            face_landmarks.landmark[263],
                            frame.shape[1],
                            frame.shape[0],
                        )

                        horizontal_ok, vertical_ok = (
                            head_controller.is_head_position_valid(
                                face_landmarks.landmark, frame.shape[1], frame.shape[0]
                            )
                        )

                        distance_ok, distance = head_controller.is_distance_valid(
                            pixel_face_width
                        )

                        MessageService.display_feedback(
                            display_frame,
                            horizontal_ok,
                            vertical_ok,
                            distance_ok,
                            distance,
                            debug_mode,
                        )

                        if horizontal_ok and vertical_ok and distance_ok:
                            dataset[grid_label].append(
                                {
                                    "point": point,
                                    "distance": distance,
                                    "landmarks": [
                                        {"x": lm.x, "y": lm.y, "z": lm.z}
                                        for lm in face_landmarks.landmark
                                    ],
                                }
                            )
                            cv2.imwrite(
                                image_filename_format.format(
                                    dot_idx=len(dataset[grid_label]) - 1,
                                    sample_idx=sample_count,
                                ),
                                clear_frame,
                            )
                            sample_count += 1

                if not debug_mode and not adjust_mode:
                    display_frame = apply_gray_overlay(display_frame)
                    draw_dot(display_frame, point, frame.shape[1], frame.shape[0])

                cv2.imshow(window_name, display_frame)
                adjust_mode = False
                if cv2.waitKey(1) == 27:  # ESC to exit
                    cap.release()
                    cv2.destroyAllWindows()
                    return

        start_time = time.time()
        while time.time() - start_time < 3:  # Wait for 3 seconds
            success, frame = cap.read()
            if not success:
                print("Ignoring empty frame.")
                continue

            display_frame = frame.copy()
            MessageService.display_message(
                display_frame,
                f"Finished {grid_label} grid calibration. Moving to the next step...",
                (50, 50),
            )
            cv2.imshow(window_name, display_frame)

            if cv2.waitKey(1) == 27:
                cap.release()
                cv2.destroyAllWindows()
                return

    cap.release()
    cv2.destroyAllWindows()

    with open(dataset_file, "w") as f:
        json.dump(dataset, f, indent=4)

    if zip_output:
        shutil.make_archive(dataset_dir, "zip", dataset_dir)

    if clean:
        shutil.rmtree(dataset_dir)
