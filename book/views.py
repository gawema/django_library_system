from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import logging
from datetime import date
from dateutil.relativedelta import relativedelta

from .models import Book, Loan

logger = logging.getLogger(__name__)

@login_required
def index(request):
	books = Book.objects.all()
	available_books = Book.objects.filter(booked=False)
	non_available_books = Book.objects.filter(booked=True)
	loans =  Loan.objects.all()
	context = {
		'user': request.user,
		'books': books,
		'aBooks': available_books,
		'bBooks': non_available_books,
		'loans': loans 
	}
	return render(request, 'book/index.html', context)

@login_required
def loanBook(request):
	if request.method == "POST":
		id = request.POST["id"]
		book = get_object_or_404(Book, pk=id)
		book.booked = True
		book.save()

		loan = Loan()
		loan.customer = request.user
		loan.book = book
		loan.startDate = date.today()
		loan.endDate = date.today()+ relativedelta(months=1)
		loan.save()


	return HttpResponseRedirect(reverse('book:index'))

@login_required
def returnBook(request): 
	if request.method == "POST":
		id = request.POST["id"]
		book = get_object_or_404(Book, pk=id)
		book.booked = False
		book.save()

		loan = get_object_or_404(Loan, book=book)
		loan.delete()


	return HttpResponseRedirect(reverse('book:index'))