from django.urls import path
from .views import homePage,aboutPage,servicePage,contactPage,blogPage

urlpatterns = [
    path('', homePage, name='home'),
    path('about/',aboutPage, name='about'),
    path('service/',servicePage, name='service'),
    path('contact/',contactPage, name='contact'),
    path('blog/',blogPage, name='blog'),
]