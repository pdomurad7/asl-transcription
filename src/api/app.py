from pathlib import Path

from fastapi import FastAPI, UploadFile, Form, File, Depends
from fastapi.staticfiles import StaticFiles
from uvicorn import run
from uuid import uuid4
from src.api.pydantic_models import TranscriptionConfigInput, TranscriptionConfig

app = FastAPI()
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")


@app.get("/")
def root():
    return "asl-transcript api"


@app.post("/file")
async def create_upload_file(file: UploadFile = File(...),
                             transcription_config: TranscriptionConfigInput = Depends()):
    file_path = f"../../files_db/{str(uuid4())}"
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    config = TranscriptionConfig(file_path=file_path, **transcription_config.dict())
    print(config)

    # Process the configuration as needed

    return {"filename": file.filename}

if __name__ == "__main__":
    run("app:app", reload=True)
