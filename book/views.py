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
def home(request):
	available_books = Book.objects.filter(booked=False, magazine=False)
	available_magazines = Book.objects.filter(booked=False, magazine=True)

	context = {
		'user': request.user,
		'books': available_books,
		'magazines': available_magazines
	}
	return render(request, 'book/home.html', context)

@login_required
def loans(request):
	loans =  Loan.objects.filter(customer = request.user)
	today = date.today()
	context = {
		'user': request.user,
		'loans': loans,
		'today': today
	}
	return render(request, 'book/loans.html', context)


@login_required
def requestBook(request):
	logger.error('HERE')
	loans = Loan.objects.filter(customer = request.user)
	bookCount = 0
	outstandings = 0
	for loan in loans:
		if loan.book.magazine == False:
			bookCount += 1
		if loan.endDate < date.today():
			outstandings += 1
	if bookCount >= 10 or outstandings >= 1:
		logger.error("ciaooo")
		return HttpResponseRedirect(reverse('book:home'))
	return confirmLoan(request, 'book')


@login_required
def requestMagazine(request):
	loans = Loan.objects.filter(customer = request.user)
	magazineCount = 0
	outstandings = 0

	for loan in loans:
		if loan.book.magazine == True:
			magazineCount += 1
		if loan.endDate <= date.today():
			outstandings += 1
	if magazineCount >= 3 or outstandings >= 1:
		return HttpResponseRedirect(reverse('book:home'))
	return confirmLoan(request, 'magazine')


@login_required
def confirmLoan(request, type):
	if request.method == "POST":
		id = request.POST["id"]
		book = get_object_or_404(Book, pk=id)
		book.booked = True
		book.save()

		loan = Loan()
		loan.customer = request.user
		loan.book = book
		loan.startDate = date.today()
		if (type == 'magazine'):
			loan.endDate = date.today() + relativedelta(days=7)
		elif (type == 'book'):
			loan.endDate = date.today() + relativedelta(months=1)
		
		loan.save()

	return HttpResponseRedirect(reverse('book:home'))

@login_required
def returnBook(request): 
	if request.method == "POST":
		id = request.POST["id"]
		loan = get_object_or_404(Loan, pk=id)
		bookId = loan.book.id;
		book = get_object_or_404(Book, pk=bookId)
		book.booked = False
		book.save()
		loan.delete()

	return HttpResponseRedirect(reverse('book:loans'))
