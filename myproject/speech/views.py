import subprocess
import os
import uuid
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

MODEL_PATH = r"C:\PythonProject\piper-models\ar\ar_JO\kareem\medium\ar_JO-kareem-medium.onnx"
PIPER_CMD = r"C:\PythonProject\venv\Scripts\piper.exe"

@csrf_exempt
def text_to_speech(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data.get('text', '').strip()
        if not text:
            return HttpResponse('No text', status=400)

        out_name = f"speech_{uuid.uuid4().hex}.wav"
        out_path = os.path.join(os.path.dirname(__file__), out_name)

        proc = subprocess.Popen(
            [PIPER_CMD, '--model', MODEL_PATH, '--output_file', out_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )
        proc.communicate(input=text)

        with open(out_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='audio/wav')
            response['Content-Disposition'] = 'inline; filename=speech.wav'

        os.remove(out_path)
        return response

    return HttpResponse('Method not allowed', status=405)