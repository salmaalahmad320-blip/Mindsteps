from django.urls import path
from .views import question_view, speak, result_view, analyze_view, home_view

urlpatterns = [
    path('', home_view, name='home'),              # 👈 مهم
    path('question/', question_view, name='question'),  # 👈 الحل هنا
    path('speak/', speak, name='speak'),
    path('result/', result_view, name='result'),
    path('analyze/', analyze_view, name='analyze'),
]