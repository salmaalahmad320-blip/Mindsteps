def validate_analysis(analysis, responses):

    total = len(responses)
    correct = sum(1 for r in responses if r["is_correct"])
    score = (correct / total) * 100 if total > 0 else 0

    # ❗ إزالة التكرار
    parts = analysis.split("تقرير التمييز السمعي")
    if len(parts) > 2:
        analysis = "تقرير التمييز السمعي" + parts[1]

    # ❗ إضافة ملاحظة (إذا مش موجودة)
    if "⚠️ ملاحظة" not in analysis:
        if score < 60:
            analysis += "\n\n⚠️ ملاحظة: يحتاج الطفل إلى متابعة وتدريب مستمر."
        else:
            analysis += "\n\n⚠️ ملاحظة: الأداء جيد ويُنصح بالاستمرار في التدريب."

    return analysis