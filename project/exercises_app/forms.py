from decimal import Decimal

from django import forms
from django.contrib.auth import get_user_model, authenticate, login
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.http import HttpResponse

from .models import Message, SCHOOL_CLASS, Student, SchoolSubject, GRADES, StudentNotice


def validate_year_of_birth(value):
    if value > 2005 or value < 2000:
        raise ValidationError(f"Rok {value} jest z poza zakresu: 2000-2004 !")


def validate_female_name(value):
    if value[-1] != 'a':
        raise ValidationError(f"Imię {value} nie jest żeńskie !")


def validate_number(value):
    if value < 1 or value > 100:
        raise ValidationError(f"Liczba {value} nie jest w zakresie 1-100")


class SearchStudentForm(forms.Form):
    last_name = forms.CharField(label='Podaj nazwisko')


class AddStudentForm(forms.Form):
    first_name = forms.CharField(label='Imię')
    last_name = forms.CharField(label='Nazwisko')
    school_class = forms.ChoiceField(choices=SCHOOL_CLASS, label='klasa')
    year_of_birth = forms.IntegerField(label='Rok urodzenia', validators=[validate_year_of_birth, ])


class ExchangeForm(forms.Form):
    CONVERSION = (
        (Decimal(0.26), "PLNtoUSD"),
        (Decimal(3.83), "USDtoPLN")
    )
    currency1 = forms.DecimalField(label="PLN", max_digits=7, decimal_places=2, required=False)
    currency2 = forms.DecimalField(label="USD", max_digits=7, decimal_places=2, required=False)
    conversion = forms.ChoiceField(choices=CONVERSION)


class AddStudentGradeForm(forms.Form):
    student = forms.ModelChoiceField(queryset=Student.objects.all())
    subject = forms.ModelChoiceField(queryset=SchoolSubject.objects.all())
    grade = forms.ChoiceField(choices=GRADES)


class PizzaToppingForm(forms.Form):
    TOPPINGS = [
        ('oliwki', 'Oliwki'),
        ('pomidory', 'Pomidory'),
        ('+ser', 'Ekstra ser'),
        ('anchovies', 'Anchovies'),
        ('cebula', 'Cebula')
    ]
    tops = forms.MultipleChoiceField(choices=TOPPINGS, widget=forms.CheckboxSelectMultiple)


class PresenceForm(forms.Form):
    student = forms.ModelChoiceField(queryset=Student.objects.all())
    day = forms.DateField(widget=forms.HiddenInput)
    present = forms.BooleanField(widget=forms.CheckboxInput, required=False)


class SetColorForm(forms.Form):
    COLOR = (
        ('black', 'black'), ('white', 'white'), ('red', 'red'), ('yellow', 'yellow'), ('blue', 'blue')
    )
    background_color = forms.ChoiceField(choices=COLOR, widget=forms.RadioSelect)


class UserDataForm(forms.Form):
    name = forms.CharField()
    last_name = forms.CharField()
    mail = forms.EmailField(validators=[EmailValidator(message='Podaj coś innego')])
    website = forms.URLField()


class SubjectForm(forms.ModelForm):
    class Meta:
        model = SchoolSubject
        fields = ('name', 'teacher_name', )


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'content', 'receiver', 'sender']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['receiver'] == cleaned_data['sender']:
            raise ValidationError('Nie możesz wysłać wiadomiści do samego '
                                  'siebie')


class LoginForm(forms.Form):
    login = forms.CharField(max_length=64)
    password = forms.CharField(max_length=64, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['login'] != 'root' and cleaned_data['password'] != 'very_secret':
            raise ValidationError("A sio, hackerze !")


class FemaleNameForm(forms.Form):
    first_name = forms.CharField(max_length=64, validators=[validate_female_name])
    last_name = forms.CharField(max_length=64)


class NumberAndStringForm(forms.Form):
    number = forms.IntegerField(validators=[validate_number])
    string = forms.CharField(max_length=128)


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=32)
    password = forms.CharField(widget=forms.PasswordInput, max_length=64)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data['username']
        password = cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is None:
            self.add_error(None, 'Podaj poprawny login lub hasło')

    def login(self, request):
        user = authenticate(**self.cleaned_data)
        return login(request, user)


class AddUserForm(forms.ModelForm):
    confirmation_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'password', )
        widgets = {
            'password': forms.PasswordInput
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['confirmation_password']:
            self.add_error('confirmation_password', "Hasła nie są identyczne !")
        if get_user_model().objects.filter(username=cleaned_data['username']):
            self.add_error('username', "Użytkownik o podanej nazwie już istnieje !")
        if get_user_model().objects.filter(email=cleaned_data['email']):
            self.add_error('email', "Użytkownik o podanym emailu już istnieje !")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class ChangePasswordForm(forms.ModelForm):
    confirmation_new_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ('password', )
        labels = {
            'password': 'new password',
        }
        widgets = {
            'password': forms.PasswordInput,
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['confirmation_new_password']:
            self.add_error('confirmation_new_password', "Hasła nie są identyczne !")


class StudentNoticeForm(forms.ModelForm):
    class Meta:
        model = StudentNotice
        fields = ['content', 'to_who', 'from_who']