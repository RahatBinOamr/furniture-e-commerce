from django.urls import path
from .views import product_view,add_to_cart,view_cart
urlpatterns =[
  path('shop/',product_view, name='shop'),
  path('add-to-cart/<slug:slug>/', add_to_cart, name='add_to_cart'),
  path('cart/', view_cart, name='view_cart'),
]