from django.db import models

class Book(models.Model):
	title = models.CharField(max_length=200)
	booked = models.BooleanField(default=False)

	def __str__(self):
		return self.title

class Loan(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE, default='')
	# customer = models.ForeignKey(User)
	startDate = models.DateField()
	endDate = models.DateField()