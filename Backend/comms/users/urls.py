from django.urls import path

from .views import RegisterBuyerView, RegisterSellerView,LoginView, SendEmail, TwitterAuthenticationView,InstagramAuthenticationView,FacebookAuthenticationView

urlpatterns = [
    path('registerSeller/', RegisterSellerView.as_view(), name='register-user'),
    path('registerBuyer/', RegisterBuyerView.as_view(), name='register-user'),
    path('login/', LoginView.as_view(), name='login-user'),
    path('send-email/', SendEmail.as_view(), name='send-email'),
    path('auth/twitter/', TwitterAuthenticationView.as_view(), name='twitter-auth'),
    path('auth/instagram/', InstagramAuthenticationView.as_view(), name='instagram-auth'),
    path('auth/facebook/', FacebookAuthenticationView.as_view(), name='facebook-auth'),
]

