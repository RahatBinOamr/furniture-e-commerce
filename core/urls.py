from django.urls import path
from .views import homePage,aboutPage,servicePage,contactPage

urlpatterns = [
    path('', homePage, name='home'),
    path('about/',aboutPage, name='about'),
    path('service/',servicePage, name='service'),
    path('contact/',contactPage, name='contact'),
]