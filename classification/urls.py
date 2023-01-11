from django.urls import path, include
from . import views



urlpatterns = [
    path('heart/', views.classification, name="dave"),
    path('', views.index, name='index')
    # path('dengue/', views.dengue, name="dengue")
]





