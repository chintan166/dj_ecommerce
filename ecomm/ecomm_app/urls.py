from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('all-product/', views.product_list, name='product_list'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('contact/', views.contact_view, name='contact'),
    path('contact/thanks/', views.contact_thanks, name='contact_thanks'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order/success/', views.order_success, name='order_success'),
    path('increment_quantity/<int:cart_item_id>/', views.increment_quantity, name='increment_quantity'),
    path('decrement_quantity/<int:cart_item_id>/', views.decrement_quantity, name='decrement_quantity'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
]