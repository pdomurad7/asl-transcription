import cv2 as cv
import numpy as np
from tensorflow.keras.models import load_model
import mediapipe as mp

from src.letter_detection.nn_model_utils.letters import Letters
from src.video_transcription.points_normalization import normalize_lists


def draw_circles(xs, ys, radius=10, img_size=480):
    img = np.zeros((img_size, img_size, 3), dtype=np.uint8)

    for x, y in zip(xs, ys):
        x = int(x * img_size)
        y = int(y * img_size)
        cv.circle(img, (x, y), radius, (255, 0, 0), -1)

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

model = load_model("../nn_model_training/models/video_dataset_fhpq_no_rotate_xyz.keras")

while True:
    success, img = cap.read()
    if not success:
        break

    h, w, _ = img.shape
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    results = hands.process(imgRGB)
    img_circle = np.zeros((480, 480, 3), dtype=np.uint8)

    if results.multi_hand_landmarks:
        handLms = results.multi_hand_landmarks[0]
        mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
        xs = [p.x for p in handLms.landmark]
        ys = [p.y for p in handLms.landmark]
        zs = [p.z for p in handLms.landmark]
        normalized_xs, normalized_ys = normalize_lists(xs, ys)
        img_circle = draw_circles(normalized_xs, normalized_ys)

        data_to_predict = np.array([normalized_xs + normalized_ys + zs])
        prediction = model.predict(data_to_predict)
        print(Letters(np.argmax(prediction[0])).name)
        cv.putText(
            img,
            str(Letters(np.argmax(prediction[0]))),
            (50, 50),
            cv.FONT_HERSHEY_SIMPLEX,
            1,
            (128, 0, 255),
            2,
            cv.LINE_AA,
        )
        cv.putText(
            img,
            str(prediction[0][np.argmax(prediction[0])]),
            (50, 100),
            cv.FONT_HERSHEY_SIMPLEX,
            1,
            (128, 0, 255),
            2,
            cv.LINE_AA,
        )

    # Wyświetlenie obrazu
    cv.imshow("Image", np.concatenate((img, img_circle), axis=1))

    # Wyjście z pętli po naciśnięciu klawisza 'q'
    if cv.waitKey(1) & 0xFF == ord("q"):
        cap.release()
        break
