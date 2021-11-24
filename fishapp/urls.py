from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from .views import (
    CategoryView,
    BaseView,
    CatalogView,
    CartView,
    AddToCartView,
    DeleteFromCartView,
    ChangeQTYView,
    CheckoutView,
    MakeOrderView,
    ProductDetailView,
    LoginView,
    RegisterView,
)
from django.views.generic import RedirectView

FAVICON_URL = '../../media/assets/favicon/favicon.ico'

try:
    from fishop import prod_settings
    if prod_settings:
        FAVICON_URL = 'media/assets/favicon/favicon.ico'
except ImportError:
    pass


urlpatterns = [
    path('', BaseView.as_view(), name='homepage'),
    path('category/<str:slug>/', CategoryView.as_view(), name='category'),
    path('category/<str:slug>/<str:sub_slug>/', CatalogView.as_view(), name='catalog'),
    path('search_result/', CatalogView.as_view(), name='search'),

    path('product/<str:slug>/<str:sub_slug>/<int:pk>/', ProductDetailView.as_view(), name='product'),
    path('product/<str:slug>/<int:pk>/', ProductDetailView.as_view(), name='product'),

    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:slug>/<int:pk>/', AddToCartView.as_view(), name='add_to_cart'),
    path('add-to-cart/<str:slug>/<str:sub_slug>/<int:pk>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from-cart/<str:slug>/<int:pk>/', DeleteFromCartView.as_view(), name='remove_from_cart'),
    path('remove-from-cart/<str:slug>/<str:sub_slug>/<int:pk>/', DeleteFromCartView.as_view(), name='remove_from_cart'),
    path('change-qty/<int:pk>/', ChangeQTYView.as_view(), name='change_qty'),

    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('make-order/', MakeOrderView.as_view(), name='make_order'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),


    path('favicon.ico', RedirectView.as_view(url=FAVICON_URL), name='favicon'),
]
