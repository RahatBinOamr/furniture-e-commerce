from django.urls import path
from . import views

urlpatterns = [
    path('assistant', views.assistant, name='assistant'),
    path('voice-query/', views.voice_query, name='voice_query'),
    path('product/<slug:slug>/', views.product_detail, name='product_details'),
]
