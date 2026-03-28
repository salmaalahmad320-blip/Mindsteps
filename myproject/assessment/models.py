from django.db import models


# 🟢 جدول الأسئلة
class Question(models.Model):
    word1 = models.CharField(max_length=100)
    word2 = models.CharField(max_length=100)
    correct_answer = models.CharField(max_length=20)  # متشابه / مختلف

    def __str__(self):
        return f"{self.word1} - {self.word2}"


# 🟡 إجابات الطفل
class Response(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    child_answer = models.CharField(max_length=20)
    is_correct = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    session_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.question} | {self.child_answer}"


# 🔵 تقرير الطفل (الجديد 🔥)
class Report(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    score = models.FloatField()
    total_questions = models.IntegerField()
    correct_answers = models.IntegerField()

    analysis = models.TextField()  # تقرير AI

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.score}%"