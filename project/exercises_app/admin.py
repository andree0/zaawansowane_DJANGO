from django.contrib import admin

from .models import SchoolSubject, Student, StudentGrades


@admin.register(SchoolSubject)
class SchoolSubjectAdmin(admin.ModelAdmin):
    list_display = ['name', ]


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(StudentGrades)
class StudentGradesAdmin(admin.ModelAdmin):
    pass
