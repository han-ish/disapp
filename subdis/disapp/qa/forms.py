#-*- coding: utf-8 -*-

from django import forms

USER_CHOICES = (
	( 'citizen', 'Citizen'),
	('student', 'Student'),
	('social worker', 'Social Worker'),
	('publice health professional', 'Public Health Professional'),
	('researcher', 'Researcher'),
		)

class LoginForm(forms.Form):
	#gps_data = forms.CharField(max_length=100)
	usergroup = forms.ChoiceField(choices=USER_CHOICES)
	email = forms.EmailField(required=True)
	org = forms.CharField(max_length=100, required=True, initial='NA')




