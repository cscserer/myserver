from django.urls import path
from django.views.static import serve

from . import views


app_name = 'projects'
urlpatterns = [
    path('', views.index, name='index'),
    path('first/', views.first, name='first'),
]

