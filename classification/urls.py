from django.urls import path, include
from . import views



urlpatterns = [
    path('heart/', views.classification, name="dave"),
    path('', views.index, name='index'),
    path('bikesharinginput/', views.bike_input, name='bikeindex'),
    path('bikesharing/', views.bike_output, name="regress")
]





