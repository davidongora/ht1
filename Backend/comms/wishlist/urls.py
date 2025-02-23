from django.urls import path
from .views import AddToWishlistView, RemoveFromWishlistView, ViewWishlistView

urlpatterns = [
    path('add/', AddToWishlistView.as_view(), name='add-to-wishlist'),
    path('remove/', RemoveFromWishlistView.as_view(), name='remove-from-wishlist'),
    path('view/', ViewWishlistView.as_view(), name='view-wishlist'),
]
