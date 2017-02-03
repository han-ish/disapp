from django.contrib import admin

# Register your models here.

from .models import Question, Choice, UserData

#admin.site.register(Question)
admin.site.register(Choice)
#admin.site.register(UserData)

class QuestionAdmin(admin.ModelAdmin):
	list_display = ('question', 'pub_date', 'pos')
	fields = ('question', 'pub_date', 'pos')

class UserAdmin(admin.ModelAdmin):
	list_display = ('email', 'usergroup')
	search_fields = ['email']

admin.site.register(Question, QuestionAdmin)
admin.site.register(UserData, UserAdmin)
#admin.site.register(Choice)


