from datetime import datetime
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.db.models import Avg
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView, ListView, UpdateView, DetailView

from .forms import (
    AddStudentForm,
    AddStudentGradeForm,
    ExchangeForm,
    FemaleNameForm,
    LoginForm,
    MessageForm,
    NumberAndStringForm,
    PizzaToppingForm,
    PresenceForm,
    SubjectForm,
    SearchStudentForm,
    SetColorForm,
    UserDataForm,
    UserLoginForm,
    ChangePasswordForm,
    StudentNoticeForm,
    AddUserForm
)
from .models import Message, PresenceList, SCHOOL_CLASS, Student, SchoolSubject, StudentGrades, StudentNotice

User = get_user_model()


class SchoolView(View):
    def get(self, request):
        context = {
            'school_classes': SCHOOL_CLASS
        }
        return render(request, 'exercises_app/school.html', context)


class SchoolClassView(View):
    def get(self, request, school_class):
        students = Student.objects.filter(school_class=school_class)
        context = {
            "students": students,
            "class_name": SCHOOL_CLASS[int(school_class-1)][1]
        }
        return render(request, "exercises_app/class.html", context)


class StudentView(View):
    def get(self, request, student_id):
        student = get_object_or_404(Student, pk=student_id)
        context = {
            'student': student,
        }
        return render(request, 'exercises_app/student.html', context)


class GradesStudentView(View):
    def get(self, request, student_id, subject_id):
        student = get_object_or_404(Student, pk=student_id)
        subject = get_object_or_404(SchoolSubject, pk=subject_id)
        student_grades = StudentGrades.objects.filter(student=student, school_subject=subject)
        # obliczenia po stronie bazy danych
        avg = student_grades.aggregate(Avg('grade'))
        # obliczenia po stronie pythona
        # average = sum([grade.grade for grade in student_grades]) / int(student_grades.count())
        context = {
            "student_grades": student_grades,
            "student": student,
            "subject": subject,
            "average": round(avg['grade__avg'], 2),
        }
        return render(request, "exercises_app/grades_student.html", context)


class StudentSearchView(View):
    template_name = "exercises_app/search_student.html"
    form_class = SearchStudentForm

    def get(self, request, *args, **kwargs):
        context = {'form': self.form_class()}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        students = None
        if form.is_valid():
            student_last_name = form.cleaned_data['last_name']
            students = Student.objects.filter(last_name__icontains=student_last_name)
            # wyszukaj liste studentów
        context = {
            'form': form,
            'students': students
        }
        return render(request, self.template_name, context)


class AddStudentView(View):
    template_name = "exercises_app/add_student.html"
    form_class = AddStudentForm

    def get(self, request, *args, **kwargs):
        context = {'form': self.form_class()}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            student_first_name = form.cleaned_data['first_name']
            student_last_name = form.cleaned_data['last_name']
            school_class = form.cleaned_data['school_class']
            year_of_birth = form.cleaned_data['year_of_birth']
            new_student = Student.objects.create(first_name=student_first_name,
                                                 last_name=student_last_name,
                                                 school_class=school_class,
                                                 year_of_birth=year_of_birth)
            message = f'Dodano nowego ucznia: {new_student}'
            return redirect(reverse('student_details', kwargs={'student_id': new_student.pk}))
            # dodanie studenta do klasy
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)


class ExchangeView(View):
    template_name = "exercises_app/exchange.html"
    form_class = ExchangeForm

    def get(self, request, *args, **kwargs):
        context = {'form': self.form_class()}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            convert = Decimal(form.cleaned_data['conversion'])
            if convert == Decimal(0.26):
                form = self.form_class(
                    initial={
                        'currency1': Decimal(form.cleaned_data['currency1']),
                        'currency2': round(Decimal(form.cleaned_data['currency1']) * convert, 2)
                    }
                )
            elif convert == Decimal(3.83):
                form = self.form_class(
                    initial={
                        'currency1': round(Decimal(form.cleaned_data['currency2']) * convert, 2),
                        'currency2': Decimal(form.cleaned_data['currency2'])
                    }
                )
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class AddStudentGradeView(View):
    form_class = AddStudentGradeForm
    template_name = 'exercises_app/add_student_grade.html'

    def get(self, request, *args, **kwargs):
        context = {'form': self.form_class()}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            student_grade = StudentGrades.objects.create(
                student=form.cleaned_data['student'],
                school_subject=form.cleaned_data['subject'],
                grade=form.cleaned_data['grade'],
            )
            return redirect(reverse('student_details', kwargs={'student_id': student_grade.student.pk}))
        context = {'form': form}
        return render(request, self.template_name, context)


class PizzaToppingsView(View):
    form_class = PizzaToppingForm
    template_name = 'exercises_app/pizza_topping.html'

    def get(self, request, *args, **kwargs):
        context = {'form': self.form_class()}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            pass
        context = {'form': form}
        return render(request, self.template_name, context)


class PresenceStudentView(View):
    form_class = PresenceForm
    template_name = 'exercises_app/presence_student.html'

    def get(self, request, student_id, day, *args, **kwargs):
        student = get_object_or_404(Student, pk=student_id)
        context = {'form': self.form_class(initial={'student': student, 'day': day})}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        message = None
        if form.is_valid():
            PresenceList.objects.create(
                student=form.cleaned_data['student'],
                day=form.cleaned_data['day'],
                present=form.cleaned_data['present']
            )
            message = "odnotowano obecność ucznia"
        context = {'form': form, 'message': message}
        return render(request, self.template_name, context)


class SetColorView(View):
    form_class = SetColorForm
    template_name = 'exercises_app/set_color.html'

    def get(self, request, *args, **kwargs):
        context = {'form': self.form_class()}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        color = None
        if form.is_valid():
            color = form.cleaned_data['background_color']
        context = {'form': form,
                   'color': color}
        return render(request, self.template_name, context)


class UserDataView(View):
    form_class = UserDataForm
    template_name = 'exercises_app/user_data.html'

    def get(self, request, *args, **kwargs):
        context = {'form': self.form_class()}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = {'form': form}
        if form.is_valid():
            context = {**context, **form.cleaned_data}
        return render(request, self.template_name, context)


class SubjectCreateView(CreateView):
    model = SchoolSubject
    form_class = SubjectForm
    success_url = reverse_lazy('index')


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('message')


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'exercises_app/login.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        return HttpResponse("Miło Cię widzieć")


class FemaleNameView(FormView):
    form_class = FemaleNameForm
    template_name = 'exercises_app/female_name.html'
    success_url = reverse_lazy('female')

    def form_valid(self, form):
        context = {**form.cleaned_data}
        return render(self.request, self.template_name, context)


class Exercise4View(FormView):
    form_class = NumberAndStringForm
    template_name = 'exercises_app/number_string.html'
    success_url = reverse_lazy('ex_4')

    def form_valid(self, form):
        context = {"result": (form.cleaned_data['string'] + " ") * form.cleaned_data['number']}
        return render(self.request, self.template_name, context)


class ListUserView(ListView):
    model = User


class UserLoginView(FormView):
    form_class = UserLoginForm
    success_url = reverse_lazy('products')
    template_name = 'exercises_app/login.html'

    def form_valid(self, form):
        form.login(self.request)
        return super().form_valid(form)


class UserLogoutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('index'))


class AddUserView(CreateView):
    model = User
    form_class = AddUserForm
    success_url = reverse_lazy('index')
    template_name = 'auth/register_user.html'

    def form_valid(self, form):
        url = super().form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        form.save()
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)
        return redirect(self.get_success_url())


class ResetPasswordView(PermissionRequiredMixin, UpdateView):
    model = User
    form_class = ChangePasswordForm
    success_url = reverse_lazy('index')
    template_name = 'auth/change_password.html'
    permission_required = 'auth.change_user'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = None
        return kwargs

    def form_valid(self, form):
        user = self.get_object()
        user.set_password(form.cleaned_data['password'])
        user.save()
        return HttpResponseRedirect(self.get_success_url())


class AddNoticeView(PermissionRequiredMixin, CreateView):
    model = StudentNotice
    form_class = StudentNoticeForm
    template_name = "exercises_app/addnotice_form.html"
    success_url = reverse_lazy('index')
    permission_required = 'exercises_app.add_studentnotice'


class StudentNoticeView(DetailView):
    model = Student
    template_name = "exercises_app/studentnotice_detail.html"
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        notices = StudentNotice.objects.filter(to_who=kwargs['object'].pk)
        context = {
            'notices': notices
        }
        return super().get_context_data(**context)