import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

from src.creds import TMP_PATH


def speech(meet):

    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    model_id = "openai/whisper-large-v3-turbo"

    model = AutoModelForSpeechSeq2Seq.from_pretrained( model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True)

    model.to(device)
    processor = AutoProcessor.from_pretrained(model_id)




    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        chunk_length_s=30,
        batch_size=16,
        torch_dtype=torch_dtype,
        device=device,
    )


    file_name = f'{TMP_PATH}/{meet.room_uri[21:]}.mp3'

    from IPython.display import Audio
    Audio(file_name)
    result = pipe(file_name)
    return result['text']


