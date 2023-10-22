import numpy as np
import cv2 as cv
import mediapipe as mp

from src.letter_detection.points_normalization import normalize_lists
from src.letter_detection.letters import Letter
from src.letter_detection.hand import Hand


def draw_circles(xs, ys, radius=10, img_size=480, white=False):
    if white:
        img = np.ones((img_size, img_size, 3), dtype=np.uint8) * 255
    else:
        img = np.zeros((img_size, img_size, 3), dtype=np.uint8)

    for i, (x, y) in enumerate(zip(xs, ys)):
        x = int(x * img_size)
        y = int(y * img_size)
        color_code = i % 4
        match color_code:
            case 0:
                color = (0, 0, 255)
            case 1:
                color = (0, 255, 0)
            case 2:
                color = (255, 0, 0)
            case 3:
                color = (255, 255, 0)
            case _:
                color = (0, 0, 0)
        cv.circle(img, (x, y), radius, color, -1)

    return img


cap = cv.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
)
mpDraw = mp.solutions.drawing_utils

while True:
    success, img = cap.read()
    if not success:
        break

    h, w, _ = img.shape
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    results = hands.process(imgRGB)
    img_circle = np.zeros((480, 480, 3), dtype=np.uint8)
    another_img = np.zeros((480, 480, 3), dtype=np.uint8)

    if results.multi_hand_landmarks:
        handLms = results.multi_hand_landmarks[0]
        mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
        xs = [p.x for p in handLms.landmark]
        ys = [p.y for p in handLms.landmark]
        zs = [p.z for p in handLms.landmark]

        list_normalized_xs, list_normalized_ys = normalize_lists(xs, ys)

        img_circle = draw_circles(xs, ys, radius=5)
        another_img = draw_circles(
            list_normalized_xs, list_normalized_ys, radius=5, white=False
        )
        hand = Hand(list_normalized_xs, list_normalized_ys, zs)
        letters = [
            letter.__name__
            for letter in Letter.__subclasses__()
            if letter(hand).check_rules()
        ]
        print(letters)
    cv.imshow("Image", np.concatenate((img, img_circle, another_img), axis=1))

    if cv.waitKey(1) & 0xFF == ord("q"):
        cap.release()
        break
