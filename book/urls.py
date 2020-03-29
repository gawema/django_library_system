from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
	path('loanBook', views.loanBook, name='loanBook'),
	path('returnBook', views.returnBook, name='returnBook')
]