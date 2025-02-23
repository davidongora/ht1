from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import LipaNaMpesa
from django.http import JsonResponse
from django.views import View
import json
from django.views.decorators.csrf import csrf_exempt  # Import csrf_exempt


class MpesaPaymentView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        amount = request.data.get('amount')

        if not phone_number or not amount:
            return Response({"error": "Phone number and amount are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Call the LipaNaMpesa service
        payment_response = LipaNaMpesa.post(phone_number, amount)

        if 'error' in payment_response:
            return Response(payment_response, status=status.HTTP_400_BAD_REQUEST)

        return Response(payment_response, status=status.HTTP_200_OK)



# @csrf_exempt  # Add this decorator to disable CSRF protection
class PaymentCallbackView(APIView):
    def post(self, request):
        # Handle the POST request here
        try:
            data = json.loads(request.body)
            if 'Body' in data and 'stkCallback' in data['Body']:
                callback_data = data['Body']['stkCallback']
                
                result_code = callback_data.get('ResultCode')
                result_desc = callback_data.get('ResultDesc')

                if result_code == "0":
                    self.process_successful_payment(callback_data)
                    return JsonResponse({'message': 'Payment processed successfully'}, status=200)
                else:
                    self.process_failed_payment(callback_data)
                    return JsonResponse({'message': 'Payment failed or cancelled'}, status=400)
            else:
                return JsonResponse({'message': 'Invalid callback structure'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'message': f'Error processing callback: {str(e)}'}, status=500)

    def process_successful_payment(self, callback_data):
        # Logic for successful payment
        print(f"Payment Successful: {callback_data}")

    def process_failed_payment(self, callback_data):
        # Logic for failed payment
        print(f"Payment Failed: {callback_data}")