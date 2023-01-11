from django.urls import path, include
from . import views



urlpatterns = [
    path('dave/', views.classification, name="dave")
    
]





