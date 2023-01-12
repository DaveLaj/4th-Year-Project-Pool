from django.urls import path, include
from . import views



urlpatterns = [
    path('project2/', views.project2, name='project2')
    
]