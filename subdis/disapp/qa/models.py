from __future__ import unicode_literals

from django.db import models

import datetime

# Create your models here.

# question and answers are in this section


class Question(models.Model):
	question = models.CharField(max_length=200)
	pos = models.PositiveSmallIntegerField(default=1)
	pub_date = models.DateField(default=datetime.datetime.now, blank=True)	
	def __str__(self):
		return self.question

class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice = models.CharField(max_length=200)

	def __str__(self):
		return self.choice


# session data

class UserData(models.Model):
	USER_CHOICES = (
		('citizen', 'Citizen'),
		('student', 'Student'),
		('social worker', 'Social Worker'),
		('public health', 'Public Health Professional'),
		('researcher', 'Researcher'),
			) 
	gps_data = models.CharField(max_length=100)
	usergroup = models.CharField(max_length=50, choices=USER_CHOICES)
	email = models.EmailField()
	q1 = models.CharField(max_length=1000, null=True)
	q2 = models.CharField(max_length=1000, null=True)
	q3 = models.CharField(max_length=1000, null=True)
	q4 = models.CharField(max_length=1000, null=True)
	q5 = models.CharField(max_length=1000, null=True)

	c1 = models.CharField(max_length=100, null=True)
	c2 = models.CharField(max_length=100, null=True)
	c3 = models.CharField(max_length=100, null=True)
	c4 = models.CharField(max_length=100, null=True)
	c5 = models.CharField(max_length=100, default=1)
	submit_date = models.DateField()
	
	#class Admin:
	#	list_display = ('gps_data', 'usergroup', 'email')
	#	list_filter = ('submit_date')
	#	ordering = ('-submit_date')
	#	search_fields = ('email')

	def __str__(self):
		return self.email

