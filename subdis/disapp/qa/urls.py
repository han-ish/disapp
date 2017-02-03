from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

# the urls for the app goes here


urlpatterns = [ 
		#url(r'^login/$', views.login, name='login'),
		#url(r'^disclaimer/$', views.disclaimer, name='disclaimer'),
		#url(r'^page/(\d+)/', views.page, name='page'),
		#url(r'^better/', views.better, name='better'),
		url(r'^signup/$', views.signup, name='signup'),
		url(r'^signin/$', views.signin, name='signin'),
		#url(r'^signinn/', views.signin_now, name='signin_now'),

		url(r'^disclaimer/$', views.signin_now, name='signin_now'),

		url(r'^claim/$', views.claim, name='claim'),
		url(r'^signupp/$', views.signupp, name='signupp'),
		url(r'signout/$', views.signout, name='signout'),
		#url(r'^question/', views.question, name='question'),
		url(r'^question/(\d+)/$', views.question_now, name='question_now'),
		#url(r'^last/', views.last, name='last'),

		url(r'^prevent/$', views.prevent, name='prevent'),

		url(r'^form/$', views.fetch_form, name='fetch_form'),
		] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
