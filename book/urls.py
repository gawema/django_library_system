from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'book'

urlpatterns = [
    path('', views.home, name='home'),
	path('loans', views.loans, name='loans'),
	path('loanBook', views.loanBook, name='loanBook'),
	path('returnBook', views.returnBook, name='returnBook'),
]