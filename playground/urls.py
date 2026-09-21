from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.show_homepage, name='show_homepage')
]