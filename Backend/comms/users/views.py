from django.shortcuts import render
from rest_framework.views import APIView
from django.db import connection
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from rest_framework_simplejwt.tokens import RefreshToken
from webpush import send_user_notification
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import requests
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import logging
import re
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError


logger = logging.getLogger(__name__)

class RegisterBuyerView(APIView):
    @swagger_auto_schema(
        operation_description="Register a new buyer",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'phone': openapi.Schema(type=openapi.TYPE_STRING),
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'subscription': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description='Push notification subscription info'
                ),
            },
            required=['email', 'phone', 'username', 'password']
        ),
        responses={
            201: openapi.Response(description="Buyer registered successfully"),
            400: openapi.Response(description="Bad request")
        }
    )
    def post(self, request):
        email = request.data.get('email')
        phone = request.data.get('phone')
        username = request.data.get('username')
        password = request.data.get('password')
        subscription_info = request.data.get('subscription')

        if not all([email, phone, username, password]):
            return Response(
                {"detail": "All fields (email, phone, username, password) are required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        with connection.cursor() as cursor:
            # Check for existing email
            cursor.execute("SELECT COUNT(*) FROM Buyers WHERE Email = %s", [email])
            if cursor.fetchone()[0] > 0:
                return Response(
                    {"detail": "Email already registered"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Check for existing phone
            cursor.execute("SELECT COUNT(*) FROM Buyers WHERE Phone = %s", [phone])
            if cursor.fetchone()[0] > 0:
                return Response(
                    {"detail": "Phone number already registered"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Check for existing username
            cursor.execute("SELECT COUNT(*) FROM Buyers WHERE username = %s", [username])
            if cursor.fetchone()[0] > 0:
                return Response(
                    {"detail": "Username already taken"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Hash password and insert new buyer
            hashed_password = make_password(password)
            cursor.execute('''
                INSERT INTO Buyers (Email, Phone, username, password) 
                VALUES (%s, %s, %s, %s)
            ''', [email, phone, username, hashed_password])

            # Send welcome email
            subject = "Welcome to Hello Tractor Marketplace"
            message = f"""
            Hi {username},

            Thank you for registering as a buyer on Hello Tractor Marketplace! 
            You can now browse and purchase tractors and implements on our platform.

            Best regards,
            Hello Tractor Team
            """
            try:
                send_mail(
                    subject,
                    message,
                    'ongoradavid5@gmail.com',
                    [email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Failed to send welcome email: {str(e)}")

            # Send push notification if subscription info is provided
            if subscription_info:
                try:
                    payload = {
                        "head": "Welcome to Hello Tractor Marketplace!",
                        "body": f"Hi {username}, thank you for joining our platform!",
                        "icon": "/static/icon.png",  # Make sure to have this icon
                        "url": "/dashboard"  # URL to redirect when notification is clicked
                    }
                    send_user_notification(
                        user=request.user,
                        payload=payload,
                        ttl=1000,
                        subscription_info=subscription_info
                    )
                except Exception as e:
                    print(f"Failed to send push notification: {str(e)}")

            return Response(
                {"detail": "Buyer registered successfully"}, 
                status=status.HTTP_201_CREATED
            )

class RegisterSellerView(APIView):
    @swagger_auto_schema(
        operation_description="Register a new seller",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'phone': openapi.Schema(type=openapi.TYPE_STRING),
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'company_details': openapi.Schema(type=openapi.TYPE_STRING),
                'logo': openapi.Schema(type=openapi.TYPE_STRING),
                'description': openapi.Schema(type=openapi.TYPE_STRING),
                'subscription': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description='Push notification subscription info'
                ),
            },
            required=['email', 'phone', 'username', 'password']
        ),
        responses={
            201: openapi.Response(description="Seller registered successfully"),
            400: openapi.Response(description="Bad request")
        }
    )
    def post(self, request):
        email = request.data.get('email')
        phone = request.data.get('phone')
        username = request.data.get('username')
        password = request.data.get('password')
        company_details = request.data.get('company_details', '')
        logo = request.data.get('logo', '')
        description = request.data.get('description', '')
        subscription_info = request.data.get('subscription')

        if not all([email, phone, username, password]):
            return Response(
                {"detail": "Email, phone, username, and password are required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        with connection.cursor() as cursor:
            # Validation checks...
            cursor.execute("SELECT COUNT(*) FROM Sellers WHERE Email = %s", [email])
            if cursor.fetchone()[0] > 0:
                return Response(
                    {"detail": "Email already registered"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            cursor.execute("SELECT COUNT(*) FROM Sellers WHERE Phone = %s", [phone])
            if cursor.fetchone()[0] > 0:
                return Response(
                    {"detail": "Phone number already registered"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            cursor.execute("SELECT COUNT(*) FROM Sellers WHERE username = %s", [username])
            if cursor.fetchone()[0] > 0:
                return Response(
                    {"detail": "Username already taken"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            hashed_password = make_password(password)
            cursor.execute('''
                INSERT INTO Sellers (Email, Phone, username, password, CompanyDetails, Logo, Description) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', [email, phone, username, hashed_password, company_details, logo, description])

            # Send welcome email
            subject = "Welcome to Hello Tractor Marketplace"
            message = f"""
            Hi {username},

            Thank you for registering as a seller on Hello Tractor Marketplace! 
            You can now list your tractors and implements for sale on our platform.

            Best regards,
            Hello Tractor Team
            """
            try:
                send_mail(
                    subject,
                    message,
                    'ongoradavid5@gmail.com',
                    [email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Failed to send welcome email: {str(e)}")

            # Send push notification if subscription info is provided
            if subscription_info:
                try:
                    payload = {
                        "head": "Welcome to Hello Tractor Marketplace!",
                        "body": f"Hi {username}, ready to start selling on our platform?",
                        "icon": "/static/icon.png",
                        "url": "/seller/dashboard"
                    }
                    send_user_notification(
                        user=request.user,
                        payload=payload,
                        ttl=1000,
                        subscription_info=subscription_info
                    )
                except Exception as e:
                    print(f"Failed to send push notification: {str(e)}")

            return Response(
                {"detail": "Seller registered successfully"}, 
                status=status.HTTP_201_CREATED
            )

class LoginView(APIView):
    @swagger_auto_schema(
        operation_description="Login user (buyer or seller)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'user_type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['buyer', 'seller']
                ),
                'subscription': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description='Push notification subscription info'
                ),
            },
            required=['username', 'password', 'user_type']
        ),
        responses={
            200: openapi.Response(description="Login successful"),
            401: openapi.Response(description="Invalid credentials"),
            400: openapi.Response(description="Bad request")
        }
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user_type = request.data.get('user_type')
        subscription_info = request.data.get('subscription')

        if not all([username, password, user_type]):
            return Response(
                {"detail": "Username, password, and user type are required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if user_type not in ['buyer', 'seller']:
            return Response(
                {"detail": "Invalid user type. Must be 'buyer' or 'seller'"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        table = 'Buyers' if user_type == 'buyer' else 'Sellers'

        with connection.cursor() as cursor:
            cursor.execute(f"""
                SELECT password, {table[:-1]}ID, Email 
                FROM {table} 
                WHERE username = %s
            """, [username])
            
            result = cursor.fetchone()
            if not result or not check_password(password, result[0]):
                return Response(
                    {"detail": "Invalid credentials"}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )

            stored_password, user_id, email = result

            # Create session
            request.session['user_id'] = user_id
            request.session['user_type'] = user_type

            # Send push notification if subscription info is provided
            if subscription_info:
                try:
                    payload = {
                        "head": "Welcome Back!",
                        "body": f"Hi {username}, welcome back to Hello Tractor Marketplace!",
                        "icon": "/static/icon.png",
                        "url": f"/{user_type}/dashboard"
                    }
                    send_user_notification(
                        user=request.user,
                        payload=payload,
                        ttl=1000,
                        subscription_info=subscription_info
                    )
                except Exception as e:
                    print(f"Failed to send push notification: {str(e)}")

            return Response({
                "detail": "Login successful",
                "user_id": user_id,
                "email": email,
                "user_type": user_type
            }, status=status.HTTP_200_OK)
class SendEmail(APIView):
    @swagger_auto_schema(
        operation_description="Send emails to users",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'recipient_email': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Email address of the recipient"
                ),
                'subject': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Email subject"
                ),
                'message': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Email message content"
                ),
            },
            required=['recipient_email', 'subject', 'message']
        ),
        responses={
            200: openapi.Response(
                description="Email sent successfully",
                examples={
                    "application/json": {
                        "success": "Email sent successfully!"
                    }
                }
            ),
            400: openapi.Response(
                description="Bad request",
                examples={
                    "application/json": {
                        "error": "Invalid email format"
                    }
                }
            ),
            500: openapi.Response(
                description="Server error",
                examples={
                    "application/json": {
                        "error": "Failed to send email"
                    }
                }
            )
        }
    )
    def post(self, request):
        try:
            # Get data from request.data instead of request.POST for better API handling
            recipient_email = request.data.get('recipient_email', '').strip()
            subject = request.data.get('subject', '').strip()
            message = request.data.get('message', '').strip()

            # Validate required fields
            if not all([recipient_email, subject, message]):
                return Response({
                    "error": "All fields (recipient_email, subject, message) are required."
                }, status=status.HTTP_400_BAD_REQUEST)

            # Validate email format
            email_validator = EmailValidator()
            try:
                email_validator(recipient_email)
            except ValidationError:
                return Response({
                    "error": "Invalid email format."
                }, status=status.HTTP_400_BAD_REQUEST)

            # Validate subject length
            if len(subject) > 255:
                return Response({
                    "error": "Subject too long. Maximum 255 characters allowed."
                }, status=status.HTTP_400_BAD_REQUEST)

            # Send email
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[recipient_email],
                    fail_silently=False,
                )
                
                # Log successful email sending
                logger.info(f"Email sent successfully to {recipient_email}")
                
                return Response({
                    "success": "Email sent successfully!",
                    "details": {
                        "recipient": recipient_email,
                        "subject": subject
                    }
                }, status=status.HTTP_200_OK)

            except BadHeaderError:
                logger.error(f"Invalid header found in email to {recipient_email}")
                return Response({
                    "error": "Invalid header found."
                }, status=status.HTTP_400_BAD_REQUEST)
                
            except Exception as e:
                logger.error(f"Failed to send email to {recipient_email}: {str(e)}")
                return Response({
                    "error": "Failed to send email. Please try again later."
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            logger.error(f"Unexpected error in SendEmail view: {str(e)}")
            return Response({
                "error": "An unexpected error occurred."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import requests
import logging
from django.conf import settings
from django.db import transaction
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)

class TwitterAuthenticationView(APIView):
    @swagger_auto_schema(
        operation_description="Authenticate user with Twitter/X",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'access_token': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Twitter OAuth 2.0 access token"
                )
                # AAAAAAAAAAAAAAAAAAAAAHPJngEAAAAAYhhq3vhO8GK0Gjedxi0jPOH%2FC3o%3Dqgic3FMAtWLGGzJDrr31R176P6xgEoD6vqYY4TR8WzVNEIJ0nR
            },
            required=['access_token']
        ),
        responses={
            200: openapi.Response(description="Authentication successful"),
            401: openapi.Response(description="Authentication failed"),
            500: openapi.Response(description="Server error")
        }
    )
    def post(self, request):
        try:
            access_token = request.data.get('access_token', 'AAAAAAAAAAAAAAAAAAAAAHPJngEAAAAAYhhq3vhO8GK0Gjedxi0jPOH%2FC3o%3Dqgic3FMAtWLGGzJDrr31R176P6xgEoD6vqYY4TR8WzVNEIJ0nR')
            
            if not access_token:
                return Response(
                    {"error": "Access token is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Twitter API v2 endpoint
            url = "https://api.twitter.com/2/users/me"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }

            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                
                user_data = response.json().get('data', {})
                user_id = user_data.get('id')
                username = user_data.get('username')

                if not user_id or not username:
                    raise ValidationError("Invalid user data received from Twitter")

                # Begin transaction for user creation/update
                with transaction.atomic():
                    # Here you would typically:
                    # 1. Check if user exists in your database
                    # 2. Create or update user record
                    # 3. Create session or token
                    # Example:
                    # user, created = User.objects.get_or_create(
                    #     twitter_id=user_id,
                    #     defaults={'username': username}
                    # )

                    return Response({
                        "message": f"Twitter authentication successful!",
                        "user": {
                            "twitter_id": user_id,
                            "username": username
                        }
                    }, status=status.HTTP_200_OK)

            except requests.exceptions.Timeout:
                logger.error("Twitter API timeout")
                return Response(
                    {"error": "Connection to Twitter timed out"}, 
                    status=status.HTTP_504_GATEWAY_TIMEOUT
                )
            
            except requests.exceptions.RequestException as e:
                logger.error(f"Twitter API error: {str(e)}")
                return Response(
                    {"error": "Failed to authenticate with Twitter"}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )

        except Exception as e:
            logger.error(f"Unexpected error in Twitter authentication: {str(e)}")
            return Response(
                {"error": "An unexpected error occurred"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class InstagramAuthenticationView(APIView):
    @swagger_auto_schema(
        operation_description="Authenticate user with Instagram",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'access_token': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Instagram OAuth access token"
                )
            },
            required=['access_token']
        ),
        responses={
            200: openapi.Response(description="Authentication successful"),
            401: openapi.Response(description="Authentication failed"),
            500: openapi.Response(description="Server error")
        }
    )
    def post(self, request):
        try:
            access_token = request.data.get('access_token')
            
            if not access_token:
                return Response(
                    {"error": "Access token is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            url = "https://graph.instagram.com/me"
            params = {
                "fields": "id,username",
                "access_token": access_token
            }

            try:
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                
                user_data = response.json()
                user_id = user_data.get('id')
                username = user_data.get('username')

                if not user_id or not username:
                    raise ValidationError("Invalid user data received from Instagram")

                with transaction.atomic():
                    # Handle user creation/update here
                    return Response({
                        "message": "Instagram authentication successful!",
                        "user": {
                            "instagram_id": user_id,
                            "username": username
                        }
                    }, status=status.HTTP_200_OK)

            except requests.exceptions.Timeout:
                logger.error("Instagram API timeout")
                return Response(
                    {"error": "Connection to Instagram timed out"}, 
                    status=status.HTTP_504_GATEWAY_TIMEOUT
                )
            
            except requests.exceptions.RequestException as e:
                logger.error(f"Instagram API error: {str(e)}")
                return Response(
                    {"error": "Failed to authenticate with Instagram"}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )

        except Exception as e:
            logger.error(f"Unexpected error in Instagram authentication: {str(e)}")
            return Response(
                {"error": "An unexpected error occurred"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class FacebookAuthenticationView(APIView):
    @swagger_auto_schema(
        operation_description="Authenticate user with Facebook",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'access_token': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Facebook OAuth access token"
                )
            },
            required=['access_token']
        ),
        responses={
            200: openapi.Response(description="Authentication successful"),
            401: openapi.Response(description="Authentication failed"),
            500: openapi.Response(description="Server error")
        }
    )
    def post(self, request):
        try:
            access_token = request.data.get('access_token')
            
            if not access_token:
                return Response(
                    {"error": "Access token is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            url = "https://graph.facebook.com/me"
            params = {
                "fields": "id,name,email",
                "access_token": access_token
            }

            try:
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                
                user_data = response.json()
                user_id = user_data.get('id')
                name = user_data.get('name')
                email = user_data.get('email')

                if not user_id or not name:
                    raise ValidationError("Invalid user data received from Facebook")

                with transaction.atomic():
                    # Handle user creation/update here
                    return Response({
                        "message": "Facebook authentication successful!",
                        "user": {
                            "facebook_id": user_id,
                            "name": name,
                            "email": email
                        }
                    }, status=status.HTTP_200_OK)

            except requests.exceptions.Timeout:
                logger.error("Facebook API timeout")
                return Response(
                    {"error": "Connection to Facebook timed out"}, 
                    status=status.HTTP_504_GATEWAY_TIMEOUT
                )
            
            except requests.exceptions.RequestException as e:
                logger.error(f"Facebook API error: {str(e)}")
                return Response(
                    {"error": "Failed to authenticate with Facebook"}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )

        except Exception as e:
            logger.error(f"Unexpected error in Facebook authentication: {str(e)}")
            return Response(
                {"error": "An unexpected error occurred"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )