from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
	title = models.CharField(max_length=200)
	booked = models.BooleanField(default=False)

	def __str__(self):
		return self.title

class Loan(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE, default='', unique=True)
	customer = models.ForeignKey(User, on_delete=models.CASCADE, default='')
	startDate = models.DateField()
	endDate = models.DateField()

	def __str__(self):
		return f"{self.book} - {self.customer}"