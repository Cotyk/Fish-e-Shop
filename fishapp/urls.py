from django.contrib import admin
from django.urls import path, include
from .views import index_view, base_view
from django.views.generic import RedirectView


urlpatterns = [
    path('', index_view, name='test'),
    path('1', base_view, name='base'),
    path('favicon.ico', RedirectView.as_view(url="../../media/assets/favicon/favicon.ico"), name='favicon'),
]
