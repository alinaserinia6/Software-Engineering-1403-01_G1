from django.urls import path
from . import views
app_name = 'group6'
urlpatterns = [
  path('', views.home, name='group6')

] 