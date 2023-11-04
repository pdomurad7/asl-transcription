import logging
import time
from collections import Counter

import cv2 as cv
import mediapipe as mp

from src.letter_detection.letter_detection_models import LetterDetectionModelFactory
from src.video_transcription.points_normalization import normalize_lists


class VideoTranscription:
    def __init__(self, config: dict):
        self.__config = config
        self.__logger = logging.getLogger(self.__class__.__name__)
        self.__letter_detection_model = LetterDetectionModelFactory().create(
            self.__config["letter_detection_model"]
        )
        self.__letters_batch_size = self.__config["letters_batch_size"]
        self.__letters_amount_to_approve = self.__config["letters_amount_to_approve"]
        self.__video_path = self.__config["video_path"]
        self.__video = None
        self.__media_pipe_model = None
        self.__initialize_video()
        self.__initialize_media_pipe_model()

    def __initialize_video(self):
        self.__logger.info("Initializing video...")
        self.__video = cv.VideoCapture(self.__video_path)

    def __initialize_media_pipe_model(self):
        self.__logger.info("Initializing media pipe model...")
        mp_hands = mp.solutions.hands
        self.__media_pipe_model = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )

    def get_transcription(self):
        self.__logger.info("Starting transcription...")
        transcription_start_time = time.perf_counter()
        last_letter = None
        first_iteration = True
        word = ""
        last_letters = []
        while True:
            success, img = self.__video.read()
            if not success:
                break

            results = self.__media_pipe_model.process(img)

            if results.multi_hand_landmarks:
                hand_lms = results.multi_hand_landmarks[0]
                xs = [p.x for p in hand_lms.landmark]
                ys = [p.y for p in hand_lms.landmark]
                zs = [p.z for p in hand_lms.landmark]

                list_normalized_xs, list_normalized_ys = normalize_lists(xs, ys)
                letter = self.__letter_detection_model.predict(
                    list_normalized_xs, list_normalized_ys, zs
                )
                if letter is None:
                    continue

                if first_iteration:
                    last_letter = letter
                    first_iteration = False

                if len(last_letters) < self.__letters_batch_size:
                    last_letters.append(letter)
                else:
                    last_letters.pop(0)
                    last_letters.append(letter)

                counter = Counter(last_letters)
                if counter.most_common(1)[0][1] > self.__letters_amount_to_approve:
                    potential_letter = counter.most_common(1)[0][0]
                    if potential_letter != last_letter:
                        word += potential_letter
                        last_letter = potential_letter
        self.__logger.info(
            f"Transcription took {time.perf_counter() - transcription_start_time} seconds"
        )
        return word
