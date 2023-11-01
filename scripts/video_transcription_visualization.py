from collections import Counter

import cv2 as cv
import mediapipe as mp
from textblob import TextBlob

from src.letter_detection.hand import Hand
from src.letter_detection.letters import Letter
from src.letter_detection.points_normalization import normalize_lists

VIDEO_PATH = "../assets/animals.mkv"
LETTERS_BATCH_SIZE = 10
LETTERS_AMOUNT_TO_APPROVE = 5

cap = cv.VideoCapture(VIDEO_PATH)

mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
)
mpDraw = mp.solutions.drawing_utils
last_letter = None
first_iteration = True
word = ""
last_letters = []

while True:
    success, img = cap.read()
    if not success:
        break

    results = hands.process(img)

    if results.multi_hand_landmarks:
        handLms = results.multi_hand_landmarks[0]
        mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
        xs = [p.x for p in handLms.landmark]
        ys = [p.y for p in handLms.landmark]
        zs = [p.z for p in handLms.landmark]

        list_normalized_xs, list_normalized_ys = normalize_lists(xs, ys)

        hand = Hand(list_normalized_xs, list_normalized_ys, zs)
        letters = [
            letter.__name__
            for letter in Letter.__subclasses__()
            if letter(hand).check_rules()
        ]
        if len(letters) != 1:
            continue
        letter = letters[0]

        if first_iteration:
            last_letter = letter
            first_iteration = False

        if len(last_letters) < LETTERS_BATCH_SIZE:
            last_letters.append(letter)
        else:
            last_letters.pop(0)
            last_letters.append(letter)

            counter = Counter(last_letters)
            if counter.most_common(1)[0][1] > LETTERS_AMOUNT_TO_APPROVE:
                potential_letter = counter.most_common(1)[0][0]
                if potential_letter != last_letter:
                    word += potential_letter
                    last_letter = potential_letter

        cv.putText(
            img,
            f"{word}",
            (img.shape[1] // 10, img.shape[0] // 10),
            cv.FONT_HERSHEY_SIMPLEX,
            3,
            (0, 0, 0),
            8,
        )
        cv.putText(
            img,
            f"{word}",
            (img.shape[1] // 10, img.shape[0] // 10),
            cv.FONT_HERSHEY_SIMPLEX,
            3,
            (255, 255, 255),
            4,
        )

        cv.putText(
            img,
            f"{last_letters}",
            (img.shape[1] // 10, img.shape[0] // 5),
            cv.FONT_HERSHEY_SIMPLEX,
            2,
            (0, 0, 0),
            8,
        )
        cv.putText(
            img,
            f"{last_letters}",
            (img.shape[1] // 10, img.shape[0] // 5),
            cv.FONT_HERSHEY_SIMPLEX,
            2,
            (255, 255, 255),
            4,
        )

    cv.imshow("Video", cv.resize(img, (0, 0), fx=0.7, fy=0.7))
    if cv.waitKey(1) & 0xFF == ord("q"):
        break

print(word)
print("corrected word: ", TextBlob(word.lower()).correct())
