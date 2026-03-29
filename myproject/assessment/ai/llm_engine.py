import subprocess
from .prompts import build_prompt


def analyze_session(responses):
    prompt = build_prompt(responses)

    try:
        result = subprocess.run(
            ["ollama", "run", "mistral"],
            input=prompt,
            text=True,
            capture_output=True,
            encoding="utf-8",
            timeout=60
        )

        #  فشل التشغيل
        if result.returncode != 0:
            return "خطأ في تشغيل نموذج الذكاء الاصطناعي"

        output = result.stdout.strip()

        #  إذا ما رجع شيء
        if not output:
            return "لم يتم توليد تحليل"

        #  تنظيف بسيط
        output = output.replace("```", "")  # لو رجع كود بلوك
        output = output.strip()

        return output

    except subprocess.TimeoutExpired:
        return "انتهى وقت انتظار الذكاء الاصطناعي"

    except Exception as e:
        return f"خطأ في AI: {str(e)}"
