from faker import Factory

from exercises_app.models import Student, SchoolSubject as Subject, SCHOOL_CLASS


def create_name():
    fake = Factory.create("pl_PL")
    first_name = fake.first_name()
    last_name = fake.last_name()
    return first_name, last_name


def create_students():
    for school_class_key, _ in SCHOOL_CLASS:
        for kid in range(0, 20):
            first_name, last_name = create_name()
            Student.objects.create(first_name=first_name,
                                   last_name=last_name,
                                   school_class=school_class_key)


def create_subjects():
    Subject.objects.create(name="Język polski", teacher_name=" ".join(create_name()))
    Subject.objects.create(name="Matematyka", teacher_name=" ".join(create_name()))
    Subject.objects.create(name="Język angielski", teacher_name=" ".join(create_name()))
    Subject.objects.create(name="Fizyka", teacher_name=" ".join(create_name()))
    Subject.objects.create(name="Wychowanie fizyczne", teacher_name=" ".join(create_name()))
    Subject.objects.create(name="Technika", teacher_name=" ".join(create_name()))
    Subject.objects.create(name="Biologia", teacher_name=" ".join(create_name()))
    Subject.objects.create(name="Chemia", teacher_name=" ".join(create_name()))
    Subject.objects.create(name="Geografia", teacher_name=" ".join(create_name()))

