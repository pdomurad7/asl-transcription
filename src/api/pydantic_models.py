import pydantic


class ModelConfig(pydantic.BaseModel):
    model_name: str
    model_config: dict


class TranscriptionConfigInput(pydantic.BaseModel):
    letter_detection_model: ModelConfig
    letters_batch_size: int
    letters_amount_to_approve: int


class TranscriptionConfig(pydantic.BaseModel):
    file_path: str
