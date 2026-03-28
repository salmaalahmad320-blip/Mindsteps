from TTS.api import TTS

tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")

tts.tts_to_file(
    text="مرحبا كيف حالك هذا اختبار الصوت العربي",
    file_path="output.wav",
    speaker_wav="voice.wav",
    language="ar"
)

print("تم إنشاء الصوت العربي")