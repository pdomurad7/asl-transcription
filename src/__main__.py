import json
import logging
import os
import warnings

from textblob import TextBlob

from src.video_transcription.video_transcription import VideoTranscription

if __name__ == "__main__":
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
    warnings.filterwarnings("ignore")

    with open("configs/example-config.json", "r") as f:
        config = json.load(f)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    stream_handler.setFormatter(formatter)
    root_logger.addHandler(stream_handler)

    word = VideoTranscription(config).get_transcription()
    print(word)
    print("corrected word: ", TextBlob(word.lower()).correct())
