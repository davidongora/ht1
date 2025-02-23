from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection, transaction
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import logging
import uuid
import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

logger = logging.getLogger(__name__)

# Create your views here.
class TractorsListCreateView(APIView):
    """
    List all tractors or create a new one.
    """
    @swagger_auto_schema(
        operation_description="Get all tractors",
        responses={
            200: openapi.Response(description="List of all tractors"),
            500: openapi.Response(description="Server error")
        }
    )
    def get(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM Tractors
                    ORDER BY TractorID DESC
                """)
                columns = [col[0] for col in cursor.description]
                tractors = [dict(zip(columns, row)) for row in cursor.fetchall()]

                return Response({
                    "tractors": tractors,
                    "total": len(tractors)
                }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error fetching tractors: {str(e)}")
            return Response({"error": "Failed to fetch tractors"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Create a new tractor",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'price': openapi.Schema(type=openapi.TYPE_NUMBER),
                'hp_power': openapi.Schema(type=openapi.TYPE_INTEGER),
                'cc_power': openapi.Schema(type=openapi.TYPE_INTEGER),
                'image': openapi.Schema(type=openapi.TYPE_FILE),
                'description': openapi.Schema(type=openapi.TYPE_STRING),
                'reviews_and_ratings': openapi.Schema(type=openapi.TYPE_STRING),
                'category': openapi.Schema(type=openapi.TYPE_STRING),
                'stock': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=['price', 'hp_power', 'cc_power', 'stock']
        ),
        responses={
            201: openapi.Response(description="Tractor created successfully"),
            400: openapi.Response(description="Invalid input"),
            500: openapi.Response(description="Server error")
        }
    )
    def post(self, request):
        try:
            price = request.data.get('price')
            hp_power = request.data.get('hp_power')
            cc_power = request.data.get('cc_power')
            description = request.data.get('description', '')
            reviews_and_ratings = request.data.get('reviews_and_ratings', '')
            category = request.data.get('category', '')
            stock = request.data.get('stock')
            image = request.FILES.get('image')

            if not all([price, hp_power, cc_power, stock]):
                return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

            image_path = None
            if image:
                file_extension = os.path.splitext(image.name)[1]
                unique_filename = f"tractors/{uuid.uuid4()}{file_extension}"
                image_path = default_storage.save(unique_filename, ContentFile(image.read()))

            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO Tractors (Price, HpPower, CcPower, Description, ReviewsAndRatings, Category, Stock, Image)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING TractorID
                    """, [price, hp_power, cc_power, description, reviews_and_ratings, category, stock, image_path])
                    
                    tractor_id = cursor.fetchone()[0]
                    return Response({
                        "message": "Tractor created successfully",
                        "tractor_id": tractor_id
                    }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error creating tractor: {str(e)}")
            return Response({"error": "Failed to create tractor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TractorDetailView(APIView):
    """
    Retrieve, update or delete a tractor.
    """
    @swagger_auto_schema(
        operation_description="Get tractor details",
        responses={
            200: openapi.Response(description="Tractor details"),
            404: openapi.Response(description="Tractor not found"),
            500: openapi.Response(description="Server error")
        }
    )
    def get(self, request, tractor_id):
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM Tractors
                    WHERE TractorID = %s
                """, [tractor_id])
                
                row = cursor.fetchone()
                if not row:
                    return Response({
                        "error": "Tractor not found"
                    }, status=status.HTTP_404_NOT_FOUND)

                columns = [col[0] for col in cursor.description]
                tractor = dict(zip(columns, row))

                return Response(tractor, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error fetching tractor {tractor_id}: {str(e)}")
            return Response({
                "error": "Failed to fetch tractor"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Update a tractor",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'image': openapi.Schema(type=openapi.TYPE_FILE),
                'price': openapi.Schema(type=openapi.TYPE_NUMBER),
                'hp_power': openapi.Schema(type=openapi.TYPE_INTEGER),
                'cc_power': openapi.Schema(type=openapi.TYPE_INTEGER),
                'description': openapi.Schema(type=openapi.TYPE_STRING),
                'reviews_and_ratings': openapi.Schema(type=openapi.TYPE_STRING),
                'category': openapi.Schema(type=openapi.TYPE_STRING),
                'stock': openapi.Schema(type=openapi.TYPE_INTEGER),
            }
        ),
        responses={
            200: openapi.Response(description="Tractor updated successfully"),
            404: openapi.Response(description="Tractor not found"),
            500: openapi.Response(description="Server error")
        }
    )
    def put(self, request, tractor_id):
        try:
            # Handle update logic
            with transaction.atomic():
                with connection.cursor() as cursor:
                    # Dynamically build query for update
                    update_fields = []
                    params = []

                    if 'price' in request.data:
                        update_fields.append("Price = %s")
                        params.append(request.data['price'])
                    if 'hp_power' in request.data:
                        update_fields.append("HpPower = %s")
                        params.append(request.data['hp_power'])
                    if 'cc_power' in request.data:
                        update_fields.append("CcPower = %s")
                        params.append(request.data['cc_power'])
                    if 'description' in request.data:
                        update_fields.append("Description = %s")
                        params.append(request.data['description'])
                    if 'reviews_and_ratings' in request.data:
                        update_fields.append("ReviewsAndRatings = %s")
                        params.append(request.data['reviews_and_ratings'])
                    if 'category' in request.data:
                        update_fields.append("Category = %s")
                        params.append(request.data['category'])
                    if 'stock' in request.data:
                        update_fields.append("Stock = %s")
                        params.append(request.data['stock'])

                    if update_fields:
                        query = f"""
                            UPDATE Tractors 
                            SET {', '.join(update_fields)}
                            WHERE TractorID = %s
                            RETURNING TractorID
                        """
                        params.append(tractor_id)
                        cursor.execute(query, params)
                        tractor_id = cursor.fetchone()[0]
                        return Response({
                            "message": "Tractor updated successfully",
                            "tractor_id": tractor_id
                        }, status=status.HTTP_200_OK)

                    return Response({"message": "No fields to update"}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error updating tractor {tractor_id}: {str(e)}")
            return Response({
                "error": "Failed to update tractor"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Delete a tractor",
        responses={
            204: openapi.Response(description="Tractor deleted successfully"),
            404: openapi.Response(description="Tractor not found"),
            500: openapi.Response(description="Server error")
        }
    )
    def delete(self, request, tractor_id):
        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute("""
                        DELETE FROM Tractors WHERE TractorID = %s
                    """, [tractor_id])

                    return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            logger.error(f"Error deleting tractor {tractor_id}: {str(e)}")
            return Response({
                "error": "Failed to delete tractor"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SearchTractors(APIView):
    """
    Search tractors by various criteria.
    """
    @swagger_auto_schema(
        operation_description="Search tractors",
        manual_parameters=[
            openapi.Parameter('category', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('min_price', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter('max_price', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter('min_hp', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('max_hp', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('min_cc', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('max_cc', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('favorite', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
        ],
        responses={
            200: openapi.Response(description="Search results for tractors"),
            500: openapi.Response(description="Server error")
        }
    )
    def get(self, request):
        try:
            # Extract search parameters
            category = request.query_params.get('category', None)
            min_price = request.query_params.get('min_price', None)
            max_price = request.query_params.get('max_price', None)
            min_hp = request.query_params.get('min_hp', None)
            max_hp = request.query_params.get('max_hp', None)
            min_cc = request.query_params.get('min_cc', None)
            max_cc = request.query_params.get('max_cc', None)
            favorite = request.query_params.get('favorite', None)

            query = """
                SELECT * FROM Tractors
                WHERE 1=1
            """
            params = []

            # Build dynamic query based on provided parameters
            if category:
                query += " AND Category = %s"
                params.append(category)
            if min_price:
                query += " AND Price >= %s"
                params.append(min_price)
            if max_price:
                query += " AND Price <= %s"
                params.append(max_price)
            if min_hp:
                query += " AND HpPower >= %s"
                params.append(min_hp)
            if max_hp:
                query += " AND HpPower <= %s"
                params.append(max_hp)
            if min_cc:
                query += " AND CcPower >= %s"
                params.append(min_cc)
            if max_cc:
                query += " AND CcPower <= %s"
                params.append(max_cc)
            if favorite is not None:
                query += " AND Favorite = %s"
                params.append(favorite)

            query += " ORDER BY TractorID DESC"

            with connection.cursor() as cursor:
                cursor.execute(query, params)
                columns = [col[0] for col in cursor.description]
                tractors = [dict(zip(columns, row)) for row in cursor.fetchall()]

            return Response({
                "tractors": tractors,
                "total": len(tractors)
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error searching tractors: {str(e)}")
            return Response({"error": "Failed to search tractors"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
