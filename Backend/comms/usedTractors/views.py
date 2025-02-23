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

class UsedTractorsListCreateView(APIView):
    """
    List all used tractors or create a new one.
    """
    @swagger_auto_schema(
        operation_description="Get all used tractors",
        responses={
            200: openapi.Response(description="List of all used tractors"),
            500: openapi.Response(description="Server error")
        }
    )
    def get(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM UsedTractors
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
        operation_description="Create a new used tractor",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'price': openapi.Schema(type=openapi.TYPE_NUMBER),
                'hp_power': openapi.Schema(type=openapi.TYPE_INTEGER),
                'cc_power': openapi.Schema(type=openapi.TYPE_INTEGER),
                'seller_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'image': openapi.Schema(type=openapi.TYPE_FILE),
                'hours_used': openapi.Schema(type=openapi.TYPE_INTEGER),
                'location': openapi.Schema(type=openapi.TYPE_STRING),
                'description': openapi.Schema(type=openapi.TYPE_STRING),
                'reviews_and_ratings': openapi.Schema(type=openapi.TYPE_STRING),
                'category': openapi.Schema(type=openapi.TYPE_STRING),
                'stock': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=['price', 'hp_power', 'cc_power', 'hours_used', 'location', 'stock']
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
            seller_id = request.data.get('seller_id')
            hours_used = request.data.get('hours_used')
            location = request.data.get('location')
            description = request.data.get('description', '')
            reviews_and_ratings = request.data.get('reviews_and_ratings', '')
            category = request.data.get('category', '')
            stock = request.data.get('stock')
            image = request.FILES.get('image')

            if not all([price, hp_power, cc_power, hours_used, location, stock]):
                return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

            image_path = None
            if image:
                file_extension = os.path.splitext(image.name)[1]
                unique_filename = f"tractors/{uuid.uuid4()}{file_extension}"
                image_path = default_storage.save(unique_filename, ContentFile(image.read()))

            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO UsedTractors (Price, HpPower, CcPower, SellerID, HoursUsed, Location, Description, ReviewsAndRatings, Category, Stock, Image)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING TractorID
                    """, [price, hp_power, cc_power, seller_id, hours_used, location, description, reviews_and_ratings, category, stock, image_path])
                    
                    tractor_id = cursor.fetchone()[0]
                    return Response({
                        "message": "Tractor created successfully",
                        "tractor_id": tractor_id
                    }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error creating tractor: {str(e)}")
            return Response({"error": "Failed to create tractor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UsedTractorDetailView(APIView):
    """
    Retrieve, update or delete a used tractor
    """
    @swagger_auto_schema(
        operation_description="Get used tractor details",
        responses={
            200: openapi.Response(description="Used tractor details"),
            404: openapi.Response(description="Used tractor not found"),
            500: openapi.Response(description="Server error")
        }
    )
    def get(self, request, tractor_id):
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT ut.*, d.Name as DealerName 
                    FROM UsedTractors ut 
                    LEFT JOIN Dealers d ON ut.DealerID = d.DealerID
                    WHERE ut.TractorID = %s
                """, [tractor_id])
                
                row = cursor.fetchone()
                if not row:
                    return Response({
                        "error": "Used tractor not found"
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
        operation_description="Update a used tractor",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'image': openapi.Schema(type=openapi.TYPE_FILE),
                'price': openapi.Schema(type=openapi.TYPE_NUMBER),
                'power': openapi.Schema(type=openapi.TYPE_INTEGER),
                'model': openapi.Schema(type=openapi.TYPE_STRING),
                'dealer_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'condition': openapi.Schema(type=openapi.TYPE_STRING),
                'reviews_and_ratings': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            200: openapi.Response(description="Used tractor updated successfully"),
            404: openapi.Response(description="Used tractor not found"),
            500: openapi.Response(description="Server error")
        }
    )
    def put(self, request, tractor_id):
        try:
            # Check if the tractor exists
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT Image FROM UsedTractors WHERE TractorID = %s
                """, [tractor_id])
                result = cursor.fetchone()
                if not result:
                    return Response({
                        "error": "Used tractor not found"
                    }, status=status.HTTP_404_NOT_FOUND)

                old_image_path = result[0]

            # Handle image update
            image_path = old_image_path
            if 'image' in request.FILES:
                image = request.FILES['image']
                file_extension = os.path.splitext(image.name)[1]
                unique_filename = f"used_tractors/{uuid.uuid4()}{file_extension}"
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
                    if 'model' in request.data:
                        update_fields.append("Model = %s")
                        params.append(request.data['model'])
                    if 'dealer_id' in request.data:
                        update_fields.append("DealerID = %s")
                        params.append(request.data['dealer_id'])
                    if 'condition' in request.data:
                        update_fields.append("Condition = %s")
                        params.append(request.data['condition'])
                    if 'reviews_and_ratings' in request.data:
                        update_fields.append("ReviewsAndRatings = %s")
                        params.append(request.data['reviews_and_ratings'])
                    if image_path != old_image_path:
                        update_fields.append("Image = %s")
                        params.append(image_path)

                    if update_fields:
                        query = f"""
                            UPDATE UsedTractors 
                            SET {', '.join(update_fields)}
                            WHERE TractorID = %s
                            RETURNING TractorID
                        """
                        params.append(tractor_id)
                        cursor.execute(query, params)

                        # Fetch updated tractor
                        cursor.execute("""
                            SELECT ut.*, d.Name as DealerName 
                            FROM UsedTractors ut 
                            LEFT JOIN Dealers d ON ut.DealerID = d.DealerID
                            WHERE ut.TractorID = %s
                        """, [tractor_id])
                        
                        columns = [col[0] for col in cursor.description]
                        tractor = dict(zip(columns, cursor.fetchone()))

                        return Response({
                            "message": "Used tractor updated successfully",
                            "tractor": tractor
                        }, status=status.HTTP_200_OK)

                    return Response({
                        "message": "No fields to update"
                    }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error updating tractor {tractor_id}: {str(e)}")
            return Response({
                "error": "Failed to update tractor"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Delete a used tractor",
        responses={
            204: openapi.Response(description="Used tractor deleted successfully"),
            404: openapi.Response(description="Used tractor not found"),
            500: openapi.Response(description="Server error")
        }
    )
    def delete(self, request, tractor_id):
        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    # Get image path before deletion
                    cursor.execute("""
                        SELECT Image FROM UsedTractors WHERE TractorID = %s
                    """, [tractor_id])
                    result = cursor.fetchone()
                    if not result:
                        return Response({
                            "error": "Used tractor not found"
                        }, status=status.HTTP_404_NOT_FOUND)

                    image_path = result[0]

                    # Delete the used tractor
                    cursor.execute("""
                        DELETE FROM UsedTractors WHERE TractorID = %s
                    """, [tractor_id])

                    # Delete associated image if it exists
                    if image_path:
                        default_storage.delete(image_path)

                    return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            logger.error(f"Error deleting tractor {tractor_id}: {str(e)}")
            return Response({
                "error": "Failed to delete tractor"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SearchUsedTractors(APIView):
    """
    Search used tractors by various criteria.
    """
    @swagger_auto_schema(
        operation_description="Search used tractors",
        manual_parameters=[
            openapi.Parameter('category', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('min_price', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter('max_price', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter('min_hp', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('max_hp', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('min_hours', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('max_hours', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('seller_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('location', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('favorite', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
        ],
        responses={
            200: openapi.Response(description="Search results for used tractors"),
            500: openapi.Response(description="Server error")
        }
    )
    def get(self, request):
        try:
            # Extract search parameters
            category = request.query_params.get('category')
            min_price = request.query_params.get('min_price')
            max_price = request.query_params.get('max_price')
            min_hp = request.query_params.get('min_hp')
            max_hp = request.query_params.get('max_hp')
            min_hours = request.query_params.get('min_hours')
            max_hours = request.query_params.get('max_hours')
            seller_id = request.query_params.get('seller_id')
            location = request.query_params.get('location')
            favorite = request.query_params.get('favorite')

            # Build query
            query = """
                SELECT ut.*, s.username as SellerUsername, s.CompanyDetails as SellerDetails
                FROM UsedTractors ut
                LEFT JOIN Sellers s ON ut.SellerID = s.SellerID
                WHERE 1=1
            """
            params = []

            if category:
                query += " AND ut.Category = %s"
                params.append(category)
            if min_price:
                query += " AND ut.Price >= %s"
                params.append(min_price)
            if max_price:
                query += " AND ut.Price <= %s"
                params.append(max_price)
            if min_hp:
                query += " AND ut.HpPower >= %s"
                params.append(min_hp)
            if max_hp:
                query += " AND ut.HpPower <= %s"
                params.append(max_hp)
            if min_hours:
                query += " AND ut.HoursUsed >= %s"
                params.append(min_hours)
            if max_hours:
                query += " AND ut.HoursUsed <= %s"
                params.append(max_hours)
            if seller_id:
                query += " AND ut.SellerID = %s"
                params.append(seller_id)
            if location:
                query += " AND ut.Location LIKE %s"
                params.append(f"%{location}%")
            if favorite is not None:
                query += " AND ut.Favorite = %s"
                params.append(favorite)

            query += " ORDER BY ut.TractorID DESC"

            with connection.cursor() as cursor:
                cursor.execute(query, params)
                columns = [col[0] for col in cursor.description]
                tractors = [dict(zip(columns, row)) for row in cursor.fetchall()]

                if not tractors:
                    return Response({
                        "message": "No tractors with the specified conditions were found."
                    }, status=status.HTTP_200_OK)

                return Response({
                    "used_tractors": tractors,
                    "total": len(tractors)
                }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error searching used tractors: {str(e)}")
            return Response({
                "error": "Failed to search used tractors"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
