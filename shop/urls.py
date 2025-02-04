from django.urls import path
from .views import productView
urlpatterns =[
  path('shop/',productView, name='shop'),
]