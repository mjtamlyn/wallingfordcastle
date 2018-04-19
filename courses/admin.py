from django.contrib import admin

from .models import CourseSignup


@admin.register(CourseSignup)
class CourseSignup(admin.ModelAdmin):
    list_display = ['student_name', 'email', 'student_date_of_birth', 'paid']
