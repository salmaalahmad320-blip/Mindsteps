from TTS.api import TTS
import tempfile

tts_model = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")

def generate_speech(text):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        tts_model.tts_to_file(
            text=text,
            file_path=f.name,
            speaker_wav="assessment/ai/voice.wav",
            language="ar"
        )
        return f.name