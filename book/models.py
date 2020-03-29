from django.db import models

class Book(models.Model):
	title = models.CharField(max_length=200)
	booked = models.BooleanField(default=False)

	def __str__(self):
		return self.title