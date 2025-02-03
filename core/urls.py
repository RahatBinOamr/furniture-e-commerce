from django.urls import path
from .views import homePage,aboutPage

urlpatterns = [
    path('', homePage, name='home'),
    path('about/',aboutPage, name='about'),
]