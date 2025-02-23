import requests
import json
import time
# from decouple import config

class GenerateToken:
    access_token = None
    token_expiry = 0

    @classmethod
    def get(cls):
        if cls.access_token and cls.token_expiry > time.time():
            return cls.access_token

        authorization = config('Authorization')
        url = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        headers = {
            'Authorization': f'Basic {authorization}',
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            token_data = response.json()
            cls.access_token = token_data['access_token']
            cls.token_expiry = time.time() + int(token_data['expires_in'])
            return cls.access_token
        except Exception as e:
            return f'Failed to fetch token: {e}'


class LipaNaMpesa:
    @staticmethod
    def post(phone_number, amount):
        access_token = GenerateToken.get()

        if not access_token or 'error' in access_token:
            return {'error': 'Failed to get access token'}

        url = 'https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        # Match the payload with the successful Postman payload
        payload = {
    "BusinessShortCode": 5449306,
    "Password": config("Password"),
    "Timestamp": "20241008095624",
    "TransactionType": "CustomerPayBillOnline",
    "Amount": amount,
    "PartyA": 254112027035,
    "PartyB": 5449306,
    "PhoneNumber": 254112027035,
    "CallBackURL": "localhost:8000/api/payments/m/callback/",
    "AccountReference": "Mavazi clothes",
    "TransactionDesc": "Payment of X goods" 
  }

        print(payload)
        try:
            response = requests.post(url, headers=headers, json=payload)
            print(payload)

            response.raise_for_status()
            return response.json()  
        except requests.exceptions.HTTPError as http_err:
            return {'error': f'HTTP Error: {http_err}', 'response': response.text}
        except Exception as e:
            return {'error': f'Request failed: {e}'}


# # Example usage
# phone_number = 254712345678  # Replace with actual phone number
# amount = 100  # Replace with the transaction amount

# # Call the LipaNaMpesa class to initiate payment
# response = LipaNaMpesa.post(phone_number, amount)
# print(response)
