"""coderslab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from exercises_app import views as ex_views
from homework_app import views as homework_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ex_views.SchoolView.as_view(), name="index"),
    path('class/<int:school_class>/', ex_views.SchoolClassView.as_view(), name="school-class"),
    path('student/<int:student_id>/', ex_views.StudentView.as_view(), name="student_details"),
    path('grades/<int:student_id>/<int:subject_id>/', ex_views.GradesStudentView.as_view(), name="grades_student"),

    path('categories/', homework_views.CategoriesView.as_view(), name="categories"),
    path('category/<str:slug>/', homework_views.CategoryView.as_view(), name="category"),
    path('product/<int:product_id>/', homework_views.ProductView.as_view(), name="product"),

    path('student_search/', ex_views.StudentSearchView.as_view(), name="student_search"),
    path('add_student/', ex_views.AddStudentView.as_view(), name="student_add"),
    path('exchange/', ex_views.ExchangeView.as_view(), name="exchange"),
    path('add_grade/', ex_views.AddStudentGradeView.as_view(), name="add_grade"),
    path('add_toppings/', ex_views.PizzaToppingsView.as_view(), name="add_toppings"),
    path('set_color/', ex_views.SetColorView.as_view(), name="set_color"),
    path('d2_p3_e1/', ex_views.UserDataView.as_view(), name="user_data"),
    path('subject/add/', ex_views.SubjectCreateView.as_view(), name="subject_create"),
    path('send_message/', ex_views.MessageCreateView.as_view(), name="message"),
    # path('login/', ex_views.LoginView.as_view(), name="login"),
    path('d2_p3_e3/', ex_views.FemaleNameView.as_view(), name="female"),
    path('d2_p3_e4/', ex_views.Exercise4View.as_view(), name="ex_4"),

    path('add_category/', homework_views.AddCategoryView.as_view(), name="add_category"),
    path('edit_category/<str:slug>/', homework_views.EditCategoryView.as_view(), name="edit_category"),
    path('products/', homework_views.ProductsView.as_view(), name="products"),
    path('edit_product/<int:pk>/', homework_views.EditProductView.as_view(), name="edit_product"),
    path('add_product/', homework_views.AddProductView.as_view(), name="add_product"),
    path('search/', homework_views.SearchProductView.as_view(), name="search_product"),
    path('user_list/', ex_views.ListUserView.as_view(), name='user_list'),
    path('login/', ex_views.UserLoginView.as_view(), name='login'),
    path('logout/', ex_views.UserLogoutView.as_view(), name='logout'),
    path('add_user/', ex_views.AddUserView.as_view(), name='add_user'),
    path('reset_password/<int:pk>/', ex_views.ResetPasswordView.as_view(), name='reset_password'),

    path('notices/<int:pk>/', ex_views.StudentNoticeView.as_view(), name='student-notice'),
    path('add_notice/', ex_views.AddNoticeView.as_view(), name='add-notice'),

    re_path(r'^class_presence/(?P<student_id>\d+)/(?P<day>[12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))/$',
            ex_views.PresenceStudentView.as_view(), name="presence"),
]
