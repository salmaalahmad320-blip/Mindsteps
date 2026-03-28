from django.contrib import admin
from .models import Question, Response, Report

admin.site.register(Question)
admin.site.register(Response)
admin.site.register(Report)  # ← هذا أهم سطر