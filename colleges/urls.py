from django.urls import re_path
from . import views


urlpatterns = [
				re_path(r'^search/$', views.search, name = 'search'),
				re_path(r'^add/$', views.add_college, name = 'add'),]