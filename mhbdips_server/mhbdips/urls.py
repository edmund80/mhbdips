from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    home, account_login, account_update_profile,
    cart_view, about_view, products_view, contact_view, product_detail_view, account_registration_view,
    add_to_order_details, favorite, add_review, remove_from_cart, update_cart_view
)

urlpatterns = [
    path('home/', home, name='home'),
    path('register/', account_registration_view, name='register'),
    path('login/', account_login, name='login'),
    path('favorites/', favorite, name='favorite'),
    path('profile/', account_update_profile, name='profile'),
    path('profile/<int:pk>/', account_update_profile, name='profile'),
    path('about/', about_view, name='about'),
    path('cart/', cart_view, name='cart'),
    path('contact/', contact_view, name='contact'),
    path('products/', products_view, name='products'),
    path('products/<int:product_id>/', product_detail_view, name='product_detail'),
    path('add_to_order_details/', add_to_order_details, name='add_to_order_details'),
    path('reviews/<int:product_id>/', add_review, name='add_review'),
    path('update_cart/<int:item_id>/', update_cart_view, name='update_cart'),
    path('remove_from_cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
