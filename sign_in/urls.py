from django.urls import re_path
from . import views


urlpatterns = [
				re_path(r'^register/$', views.register, name = 'register'),
				re_path(r'^profile/$', views.profile, name = 'profile'),
				re_path(r'^update/$', views.update, name = 'update'),]