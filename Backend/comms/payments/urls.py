
from django.urls import path
from .views import MpesaPaymentView, PaymentCallbackView

urlpatterns = [
    path('mpesa/payment/', MpesaPaymentView.as_view(), name='mpesa-payment'),
    path('mpepe/callback/', PaymentCallbackView.as_view(), name='payment_callback'),

]