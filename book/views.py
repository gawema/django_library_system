from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
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
    if request.user.is_staff == True:
        return HttpResponseRedirect(reverse('book:allLoans'))
    available_books = Book.objects.filter(booked=False, magazine=False)
    available_magazines = Book.objects.filter(booked=False, magazine=True)
    reminders = []
    loans = Loan.objects.filter(customer=request.user)
    for loan in loans:
        if loan.reminder is not None:
            reminders.append(loan.reminder)

    context = {
        'user': request.user,
        'books': available_books,
        'magazines': available_magazines,
        'reminders': reminders
    }
    return render(request, 'book/home.html', context)


@login_required
def loans(request):
    if request.user.is_staff == True:
        return HttpResponseRedirect(reverse('book:allLoans'))
    loans = Loan.objects.filter(customer=request.user)
    today = date.today()
    context = {
        'user': request.user,
        'loans': loans,
        'today': today
    }
    return render(request, 'book/loans.html', context)


@login_required
def requestBook(request):
    loans = Loan.objects.filter(customer=request.user)
    bookCount = 0
    outstandings = 0
    for loan in loans:
        if loan.book.magazine == False:
            bookCount += 1
        if loan.endDate < date.today():
            outstandings += 1
    if bookCount >= 10 or outstandings >= 1:
        messages.info(request, 'Sorry, you can not loan more books or magazine, return some!')
        return HttpResponseRedirect(reverse('book:home'))
    return confirmLoan(request, 'book')


@login_required
def requestMagazine(request):
    loans = Loan.objects.filter(customer=request.user)
    magazineCount = 0
    outstandings = 0

    for loan in loans:
        if loan.book.magazine == True:
            magazineCount += 1
        if loan.endDate <= date.today():
            outstandings += 1
    if magazineCount >= 3 or outstandings >= 1:
        messages.info(request, 'Sorry, you can not loan more books or magazine, return some!')
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
        bookId = loan.book.id
        book = get_object_or_404(Book, pk=bookId)
        book.booked = False
        book.save()
        loan.delete()

    return HttpResponseRedirect(reverse('book:loans'))


@login_required
def oustandingLoans(request):
    if request.user.is_staff == False:
        return HttpResponseRedirect(reverse('book:home'))
    loans = Loan.objects.all()
    oustanding_loans = []
    for loan in loans:
        if loan.endDate < date.today():
            oustanding_loans.append(loan)
    context = {
        'user': request.user,
        'loans': oustanding_loans,
    }
    return render(request, 'book/oustanding_loans.html', context)


@login_required
def allLoans(request):
    if request.user.is_staff == False:
        return HttpResponseRedirect(reverse('book:home'))
    loans = Loan.objects.all()
    request.user.is_staff
    context = {
        'user': request.user,
        'loans': loans,
    }
    return render(request, 'book/all_loans.html', context)


@login_required
def sendReminder(request):
    if request.user.is_staff == False:
        return HttpResponseRedirect(reverse('book:home'))
    if request.method == "POST":
        id = request.POST["id"]
        loan = get_object_or_404(Loan, pk=id)
        loan.reminder = "Reminder: '"+loan.book.title + \
            "' needs to be returned as soon as possible"
        loan.save()

    return HttpResponseRedirect(reverse('book:oustandingLoans'))
