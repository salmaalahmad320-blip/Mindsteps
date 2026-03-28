from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Question, Response, Report
from .ai.llm_engine import analyze_session
from .ai.tts_engine import generate_speech
from .ai.validation import validate_analysis
from .ai.guardrails import sanitize_text
import random


# ✅ الصفحة الرئيسية
def home_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        age = request.POST.get("age")

        request.session["name"] = name
        request.session["age"] = age

        # 🔥 reset session
        request.session['session_id'] = str(random.random())
        request.session.pop('questions', None)
        request.session.pop('index', None)
        request.session.pop('welcomed', None)

        return redirect('question')

    return render(request, "assessment/home.html")


# ✅ صفحة الأسئلة
def question_view(request):

    if 'session_id' not in request.session:
        request.session['session_id'] = str(random.random())

    if 'questions' not in request.session:
        all_questions = list(Question.objects.all())

        if len(all_questions) < 10:
            return HttpResponse("عدد الأسئلة غير كافي")

        selected = random.sample(all_questions, 10)
        request.session['questions'] = [q.id for q in selected]
        request.session['index'] = 0

    question_ids = request.session['questions']

    questions_map = {q.id: q for q in Question.objects.filter(id__in=question_ids)}
    questions = [questions_map[qid] for qid in question_ids if qid in questions_map]

    if not questions:
        return HttpResponse("لا يوجد أسئلة")

    index = request.session.get('index', 0)
    total_questions = len(questions)

    if index >= total_questions:
        return redirect('result')

    question = questions[index]

    # 👋 ترحيب مرة واحدة
    first_time = False
    if 'welcomed' not in request.session:
        request.session['welcomed'] = True
        first_time = True

    if request.method == "POST":
        answer = request.POST.get("answer")
        is_correct = answer == question.correct_answer

        Response.objects.create(
            question=question,
            child_answer=answer,
            is_correct=is_correct,
            session_id=request.session['session_id']
        )

        request.session['index'] = index + 1
        request.session['feedback'] = "correct" if is_correct else "wrong"
        request.session.modified = True

        return redirect('question')

    feedback = request.session.pop('feedback', None)

    # حساب التقدم
    current_index = index + 1          # 1-based
    progress_percent = (index / total_questions) * 100 if total_questions > 0 else 0

    return render(request, "assessment/question.html", {
        "question": question,
        "feedback": feedback,
        "name": request.session.get("name"),
        "first_time": first_time,
        "current_index": current_index,
        "total_questions": total_questions,
        "progress_percent": progress_percent,
        "correct_answer": question.correct_answer,
    })


# ✅ الصوت
def speak(request):
    text = request.GET.get("text", "")
    file_path = generate_speech(text)

    with open(file_path, "rb") as f:
        audio = f.read()

    return HttpResponse(audio, content_type="audio/wav")


# ✅ النتيجة + AI
def result_view(request):
    session_id = request.session.get('session_id')

    responses = Response.objects.filter(
        session_id=session_id
    ).select_related('question')

    total = responses.count()
    correct = responses.filter(is_correct=True).count()
    score = (correct / total) * 100 if total > 0 else 0

    # 🔹 تجهيز البيانات للـ AI
    data = []
    for r in responses:
        data.append({
            "word1": r.question.word1,
            "word2": r.question.word2,
            "correct_answer": r.question.correct_answer,
            "child_answer": r.child_answer,
            "is_correct": r.is_correct,
        })

    # 🧠 تحليل AI
    analysis = analyze_session(data)

    # ❗ تحقق من الخطأ (نص)
    if isinstance(analysis, str) and "خطأ" in analysis:
        return render(request, "assessment/result.html", {
            "error": analysis,
            "score": round(score, 2),
            "total_questions": total,
            "correct": correct,
            "name": request.session.get("name")
        })

    # 🛡️ حماية
    analysis = validate_analysis(analysis, data)
    analysis = sanitize_text(analysis)

    # 💾 حفظ التقرير (كنص)
    Report.objects.create(
        name=request.session.get("name"),
        age=request.session.get("age"),
        score=score,
        total_questions=total,
        correct_answers=correct,
        analysis=analysis
    )

    # 🎯 عرض النتيجة
    return render(request, "assessment/result.html", {
        "analysis": analysis,
        "score": round(score, 2),
        "name": request.session.get("name"),
        "total_questions": total,
        "correct": correct
    })


# ✅ تحليل منفصل (اختياري)
def analyze_view(request):
    session_id = request.session.get('session_id')

    responses = Response.objects.filter(
        session_id=session_id
    ).select_related('question')

    data = []
    for r in responses:
        data.append({
            "word1": r.question.word1,
            "word2": r.question.word2,
            "correct_answer": r.question.correct_answer,
            "child_answer": r.child_answer,
            "is_correct": r.is_correct,
        })

    analysis = analyze_session(data)

    return render(request, "assessment/analysis.html", {
        "analysis": analysis,
        "name": request.session.get("name")
    })