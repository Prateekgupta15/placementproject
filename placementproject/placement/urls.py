from django.contrib import admin
from django.urls import path
from . import views

app_name = "placement"

urlpatterns = [
    path('',views.index,name='index'),
    path("login/", views.login, name="login"),
    # path("register/", views.register, name="register"),
    path("logout", views.logout, name="logout"),
    path("pdf_mail/", views.mail_pdf, name="pdf"),

    path("preview/", views.preview, name="preview"),

    
]