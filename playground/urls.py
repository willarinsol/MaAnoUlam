from django.urls import path
from . import views

urlpatterns = [
    path('hero/', views.show_homepage, name='show_homepage')
]