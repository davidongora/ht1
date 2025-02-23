from django.urls import path
from .views import AddCartItemView, GetCartItemsView, UpdateCartItemView, RemoveCartItemView

urlpatterns = [
    path('cart/add/', AddCartItemView.as_view(), name='add-cart-item'),
    path('cart/', GetCartItemsView.as_view(), name='get-cart-items'),
    path('cart/update/', UpdateCartItemView.as_view(), name='update-cart-item'),
    path('cart/remove/', RemoveCartItemView.as_view(), name='remove-cart-item'),
    # path('cart/total/', GetCartTotalPriceView.as_view(), name='get-cart-total-price'),
]
