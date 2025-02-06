from django.urls import path
from .views import *
urlpatterns =[
  path('shop/',product_view, name='shop'),
  path('add-to-cart/<slug:slug>/', add_to_cart, name='add_to_cart'),
  path('cart/', view_cart, name='view_cart'),
  path('increment-item/<int:id>',increment_item, name='increment_item'),
  path('decrement-item/<int:id>',decrement_item, name='decrement_item'),
  path('remove-item/<int:id>',remove_item,name='remove_item'),
  path('checkout/', checkout, name='checkout'),
  path('checkout/success/', checkout_success, name='checkout_success'),
  path('checkout/cancel/', checkout_cancel, name='checkout_cancel'),
]