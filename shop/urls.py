from django.urls import path
from .views import product_view,add_to_cart,view_cart,increment_item,decrement_item,remove_item
urlpatterns =[
  path('shop/',product_view, name='shop'),
  path('add-to-cart/<slug:slug>/', add_to_cart, name='add_to_cart'),
  path('cart/', view_cart, name='view_cart'),
  path('increment-item/<int:id>',increment_item, name='increment_item'),
  path('decrement-item/<int:id>',decrement_item, name='decrement_item'),
  path('remove-item/<int:id>',remove_item,name='remove_item')
]