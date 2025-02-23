from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection, transaction
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import logging
from decimal import Decimal
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import uuid

logger = logging.getLogger(__name__)

class ImplementListCreateView(APIView):
    """
    List all implements or create a new one
    """
    @swagger_auto_schema(
        operation_description="Get all implements",
        responses={
            200: openapi.Response(description="List of all implements"),
            500: openapi.Response(description="Server error")
        }
    )
    def get(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT i.*, d.Name as DealerName 
                    FROM Implements i 
                    LEFT JOIN Dealers d ON i.DealerID = d.DealerID
                    ORDER BY i.ImplementID DESC
                """)
                columns = [col[0] for col in cursor.description]
                implements = [dict(zip(columns, row)) for row in cursor.fetchall()]

                return Response({
                    "implements": implements,
                    "total": len(implements)
                }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error fetching implements: {str(e)}")
            return Response({
                "error": "Failed to fetch implements"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Create a new implement",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'image': openapi.Schema(type=openapi.TYPE_FILE),
                'price': openapi.Schema(type=openapi.TYPE_NUMBER),
                'power': openapi.Schema(type=openapi.TYPE_INTEGER),
                'category': openapi.Schema(type=openapi.TYPE_STRING),
                'dealer_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'reviews_and_ratings': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['price', 'power', 'category', 'dealer_id']
        ),
        responses={
            201: openapi.Response(description="Implement created successfully"),
            400: openapi.Response(description="Invalid input"),
            500: openapi.Response(description="Server error")
        }
    )
    def post(self, request):
        try:
            # Extract data from request
            price = request.data.get('price')
            power = request.data.get('power')
            category = request.data.get('category')
            dealer_id = request.data.get('dealer_id')
            reviews_and_ratings = request.data.get('reviews_and_ratings', '')
            image = request.FILES.get('image')

            # Validate required fields
            if not all([price, power, category, dealer_id]):
                return Response({
                    "error": "Price, power, category, and dealer_id are required"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Handle image upload
            image_path = None
            if image:
                file_extension = os.path.splitext(image.name)[1]
                unique_filename = f"implements/{uuid.uuid4()}{file_extension}"
                image_path = default_storage.save(unique_filename, ContentFile(image.read()))

            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO Implements 
                        (Image, Price, Power, Category, DealerID, ReviewsAndRatings)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        RETURNING ImplementID
                    """, [image_path, price, power, category, dealer_id, reviews_and_ratings])
                    
                    implement_id = cursor.fetchone()[0]

                    # Fetch the created implement
                    cursor.execute("""
                        SELECT i.*, d.Name as DealerName 
                        FROM Implements i 
                        LEFT JOIN Dealers d ON i.DealerID = d.DealerID
                        WHERE i.ImplementID = %s
                    """, [implement_id])
                    
                    columns = [col[0] for col in cursor.description]
                    implement = dict(zip(columns, cursor.fetchone()))

                    return Response({
                        "message": "Implement created successfully",
                        "implement": implement
                    }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error creating implement: {str(e)}")
            return Response({
                "error": "Failed to create implement"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ImplementDetailView(APIView):
    """
    Retrieve, update or delete an implement
    """
    @swagger_auto_schema(
        operation_description="Get implement details",
        responses={
            200: openapi.Response(description="Implement details"),
            404: openapi.Response(description="Implement not found"),
            500: openapi.Response(description="Server error")
        }
    )
    def get(self, request, implement_id):
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT i.*, d.Name as DealerName 
                    FROM Implements i 
                    LEFT JOIN Dealers d ON i.DealerID = d.DealerID
                    WHERE i.ImplementID = %s
                """, [implement_id])
                
                row = cursor.fetchone()
                if not row:
                    return Response({
                        "error": "Implement not found"
                    }, status=status.HTTP_404_NOT_FOUND)

                columns = [col[0] for col in cursor.description]
                implement = dict(zip(columns, row))

                return Response(implement, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error fetching implement {implement_id}: {str(e)}")
            return Response({
                "error": "Failed to fetch implement"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Update an implement",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'image': openapi.Schema(type=openapi.TYPE_FILE),
                'price': openapi.Schema(type=openapi.TYPE_NUMBER),
                'power': openapi.Schema(type=openapi.TYPE_INTEGER),
                'category': openapi.Schema(type=openapi.TYPE_STRING),
                'dealer_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'reviews_and_ratings': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            200: openapi.Response(description="Implement updated successfully"),
            404: openapi.Response(description="Implement not found"),
            500: openapi.Response(description="Server error")
        }
    )
    def put(self, request, implement_id):
        try:
            # Check if implement exists
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT Image FROM Implements WHERE ImplementID = %s
                """, [implement_id])
                result = cursor.fetchone()
                if not result:
                    return Response({
                        "error": "Implement not found"
                    }, status=status.HTTP_404_NOT_FOUND)

                old_image_path = result[0]

            # Handle image update
            image_path = old_image_path
            if 'image' in request.FILES:
                image = request.FILES['image']
                file_extension = os.path.splitext(image.name)[1]
                unique_filename = f"implements/{uuid.uuid4()}{file_extension}"
                image_path = default_storage.save(unique_filename, ContentFile(image.read()))
                
                # Delete old image if it exists
                if old_image_path:
                    default_storage.delete(old_image_path)

            with transaction.atomic():
                with connection.cursor() as cursor:
                    update_fields = []
                    params = []

                    # Build dynamic update query
                    if 'price' in request.data:
                        update_fields.append("Price = %s")
                        params.append(request.data['price'])
                    if 'power' in request.data:
                        update_fields.append("Power = %s")
                        params.append(request.data['power'])
                    if 'category' in request.data:
                        update_fields.append("Category = %s")
                        params.append(request.data['category'])
                    if 'dealer_id' in request.data:
                        update_fields.append("DealerID = %s")
                        params.append(request.data['dealer_id'])
                    if 'reviews_and_ratings' in request.data:
                        update_fields.append("ReviewsAndRatings = %s")
                        params.append(request.data['reviews_and_ratings'])
                    if image_path != old_image_path:
                        update_fields.append("Image = %s")
                        params.append(image_path)

                    if update_fields:
                        query = f"""
                            UPDATE Implements 
                            SET {', '.join(update_fields)}
                            WHERE ImplementID = %s
                            RETURNING ImplementID
                        """
                        params.append(implement_id)
                        cursor.execute(query, params)

                        # Fetch updated implement
                        cursor.execute("""
                            SELECT i.*, d.Name as DealerName 
                            FROM Implements i 
                            LEFT JOIN Dealers d ON i.DealerID = d.DealerID
                            WHERE i.ImplementID = %s
                        """, [implement_id])
                        
                        columns = [col[0] for col in cursor.description]
                        implement = dict(zip(columns, cursor.fetchone()))

                        return Response({
                            "message": "Implement updated successfully",
                            "implement": implement
                        }, status=status.HTTP_200_OK)
                    
                    return Response({
                        "message": "No fields to update"
                    }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error updating implement {implement_id}: {str(e)}")
            return Response({
                "error": "Failed to update implement"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Delete an implement",
        responses={
            204: openapi.Response(description="Implement deleted successfully"),
            404: openapi.Response(description="Implement not found"),
            500: openapi.Response(description="Server error")
        }
    )
    def delete(self, request, implement_id):
        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    # Get image path before deletion
                    cursor.execute("""
                        SELECT Image FROM Implements WHERE ImplementID = %s
                    """, [implement_id])
                    result = cursor.fetchone()
                    if not result:
                        return Response({
                            "error": "Implement not found"
                        }, status=status.HTTP_404_NOT_FOUND)

                    image_path = result[0]

                    # Delete the implement
                    cursor.execute("""
                        DELETE FROM Implements WHERE ImplementID = %s
                    """, [implement_id])

                    # Delete associated image if it exists
                    if image_path:
                        default_storage.delete(image_path)

                    return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            logger.error(f"Error deleting implement {implement_id}: {str(e)}")
            return Response({
                "error": "Failed to delete implement"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ImplementSearchView(APIView):
    """
    Search implements by various criteria
    """
    @swagger_auto_schema(
        operation_description="Search implements",
        manual_parameters=[
            openapi.Parameter('category', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('min_price', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter('max_price', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter('min_power', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('max_power', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('dealer_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: openapi.Response(description="Search results"),
            500: openapi.Response(description="Server error")
        }
    )
    def get(self, request):
        try:
            # Extract search parameters
            category = request.query_params.get('category')
            min_price = request.query_params.get('min_price')
            max_price = request.query_params.get('max_price')
            min_power = request.query_params.get('min_power')
            max_power = request.query_params.get('max_power')
            dealer_id = request.query_params.get('dealer_id')

            # Build query
            query = """
                SELECT i.*, d.Name as DealerName 
                FROM Implements i 
                LEFT JOIN Dealers d ON i.DealerID = d.DealerID
                WHERE 1=1
            """
            params = []

            if category:
                query += " AND i.Category = %s"
                params.append(category)
            if min_price:
                query += " AND i.Price >= %s"
                params.append(min_price)
            if max_price:
                query += " AND i.Price <= %s"
                params.append(max_price)
            if min_power:
                query += " AND i.Power >= %s"
                params.append(min_power)
            if max_power:
                query += " AND i.Power <= %s"
                params.append(max_power)
            if dealer_id:
                query += " AND i.DealerID = %s"
                params.append(dealer_id)

            query += " ORDER BY i.ImplementID DESC"

            with connection.cursor() as cursor:
                cursor.execute(query, params)
                columns = [col[0] for col in cursor.description]
                implements = [dict(zip(columns, row)) for row in cursor.fetchall()]

                return Response({
                    "implements": implements,
                    "total": len(implements)
                }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error searching implements: {str(e)}")
            return Response({
                "error": "Failed to search implements"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
