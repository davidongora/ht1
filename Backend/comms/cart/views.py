from django.db import connection, transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class AddCartItemView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'BuyerID': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the buyer", example=101),
                'ItemID': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the item", example=1),
                'Quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description="Quantity of the item", example=2),
                'Price': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL, description="Price of the item", example=50.0),
            },
            required=['BuyerID', 'ItemID', 'Quantity', 'Price'],
            examples={
                'application/json': {
                    'BuyerID': 101,
                    'ItemID': 1,
                    'Quantity': 2,
                    'Price': 50.0
                }
            }
        ),
        responses={
            201: openapi.Response(description="Item added to the cart", examples={"application/json": {"message": "Item added successfully"}}),
            400: openapi.Response(description="Bad Request", examples={"application/json": {"error": "Invalid data"}})
        }
    )
    def post(self, request):
        BuyerID = request.data.get('BuyerID')
        ItemID = request.data.get('ItemID')
        Quantity = request.data.get('Quantity')
        Price = request.data.get('Price')

        if not all([BuyerID, ItemID, Quantity, Price]):
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO CartItems (BuyerID, ItemID, Quantity, Price)
                        VALUES (%s, %s, %s, %s)
                    """, [BuyerID, ItemID, Quantity, Price])
                    connection.commit()
            return Response({'message': 'Item added successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetCartItemsView(APIView):
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="List of items in the cart",
                type=openapi.TYPE_OBJECT,
            properties={
                'BuyerID': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the cart item", example=1),
                },
                examples={
                    "application/json": [
                        {
                            "CartItemID": 1,
                            "BuyerID": 101,
                            "ItemID": 1,
                            "Quantity": 2,
                            "Price": 50.0,
                            "TotalPrice": 100.0
                        }
                    ]
                }
            ),
            
            400: openapi.Response(description="Bad Request")
        }
    )
    def get(self, request):
        BuyerID = request.query_params.get('BuyerID')

        if not BuyerID:
            return Response({'error': 'BuyerID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT CartItemID, BuyerID, ItemID, Quantity, Price, (Quantity * Price) AS TotalPrice
                    FROM CartItems
                    WHERE BuyerID = %s
                """, [BuyerID])
                cart_items = cursor.fetchall()

            cart_items_data = [
                {
                    'CartItemID': item[0],
                    'BuyerID': item[1],
                    'ItemID': item[2],
                    'Quantity': item[3],
                    'Price': item[4],
                    'TotalPrice': item[5]
                }
                for item in cart_items
            ]

            return Response(cart_items_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateCartItemView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'CartItemID': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the cart item", example=1),
                'Quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description="New quantity of the item", example=3),
                'Price': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL, description="New price of the item", example=55.0),
            },
            required=['CartItemID', 'Quantity', 'Price'],
            examples={
                'application/json': {
                    'CartItemID': 1,
                    'Quantity': 3,
                    'Price': 55.0
                }
            }
        ),
        responses={
            200: openapi.Response(description="Cart item updated", examples={"application/json": {"message": "Item updated successfully"}}),
            400: openapi.Response(description="Bad Request", examples={"application/json": {"error": "Invalid data"}}),
            404: openapi.Response(description="Cart item not found", examples={"application/json": {"error": "Item not found"}})
        }
    )
    def put(self, request):
        CartItemID = request.data.get('CartItemID')
        Quantity = request.data.get('Quantity')
        Price = request.data.get('Price')

        if not all([CartItemID, Quantity, Price]):
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute("""
                        UPDATE CartItems
                        SET Quantity = %s, Price = %s
                        WHERE CartItemID = %s
                    """, [Quantity, Price, CartItemID])
                    connection.commit()

            return Response({'message': 'Item updated successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RemoveCartItemView(APIView):
    @swagger_auto_schema(
        responses={
            200: openapi.Response(description="Item removed from the cart", examples={"application/json": {"message": "Item removed successfully"}}),
            404: openapi.Response(description="Cart item not found", examples={"application/json": {"error": "Item not found"}})
        }
    )
    def delete(self, request):
        CartItemID = request.query_params.get('CartItemID')

        if not CartItemID:
            return Response({'error': 'CartItemID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute("""
                        DELETE FROM CartItems
                        WHERE CartItemID = %s
                    """, [CartItemID])
                    connection.commit()

            return Response({'message': 'Item removed successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
