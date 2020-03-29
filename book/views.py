from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import logging

from .models import Book

logger = logging.getLogger(__name__)

def index(request):
	books = Book.objects.all()
	available_books = Book.objects.filter(booked=False)
	non_available_books = Book.objects.filter(booked=True)
	context = {
		'books': books,
		'aBooks': available_books,
		'bBooks' : non_available_books
	}
	return render(request, 'book/index.html', context)

def loanBook(request):
	if request.method == "POST":
		id = request.POST["id"]
		book = get_object_or_404(Book, pk=id)
		book.booked = True
		book.save()
	return HttpResponseRedirect(reverse('index'))

def returnBook(request): 
	if request.method == "POST":
		id = request.POST["id"]
		book = get_object_or_404(Book, pk=id)
		book.booked = False
		book.save()
	return HttpResponseRedirect(reverse('index'))