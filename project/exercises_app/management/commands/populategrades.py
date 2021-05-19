import random
from django.core.management.base import BaseCommand

from exercises_app.models import GRADES, SchoolSubject, Student, StudentGrades


def get_random_grade():
    grade = random.choice(GRADES)
    return grade[0]


class Command(BaseCommand):
    help = 'Create random grade for subject of student'

    def handle(self, *args, **options):
        for student in Student.objects.all():
            for subject in SchoolSubject.objects.all():
                StudentGrades.objects.create(
                    student=student,
                    school_subject=subject,
                    grade=get_random_grade()
                )
