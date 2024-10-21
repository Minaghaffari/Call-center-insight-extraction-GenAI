import whisper


def transcribe_whisper(sample_voice):
    model = whisper.load_model("base")
    result = model.transcribe(sample_voice)
    transcript = result['text']
    return transcript
