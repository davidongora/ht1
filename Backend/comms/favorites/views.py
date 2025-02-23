# views.py
from django.db import connection
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
import json
from django.core.paginator import Paginator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class FavoriteListView(APIView):
    @swagger_auto_schema(
        operation_description="Get all favorites with product details for a buyer",
        manual_parameters=[
            openapi.Parameter('buyer_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
        ]
    )
    def get(self, request):
        buyer_id = request.GET.get('buyer_id')
        if not buyer_id:
            return JsonResponse(
                {'error': 'buyer_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        query = """
            WITH FavoriteDetails AS (
                -- Get regular tractors details
                SELECT 
                    f.FavouriteID,
                    f.BuyerID,
                    f.ProductType,
                    f.ProductID,
                    f.CreatedAt,
                    t.Price,
                    t.HpPower,
                    t.CcPower,
                    t.Image,
                    t.Description,
                    t.Category,
                    NULL as HoursUsed,
                    NULL as Location,
                    NULL as ReviewsAndRatings,
                    NULL as SellerID,
                    'New' as TractorCondition
                FROM Favourites f
                JOIN Tractors t ON f.ProductID = t.TractorID
                WHERE f.ProductType = 'Tractors'
                AND f.BuyerID = %s

                UNION ALL

                -- Get used tractors details
                SELECT 
                    f.FavouriteID,
                    f.BuyerID,
                    f.ProductType,
                    f.ProductID,
                    f.CreatedAt,
                    ut.Price,
                    ut.HpPower,
                    ut.CcPower,
                    ut.Image,
                    ut.Description,
                    ut.Category,
                    ut.HoursUsed,
                    ut.Location,
                    ut.ReviewsAndRatings,
                    ut.SellerID,
                    'Used' as TractorCondition
                FROM Favourites f
                JOIN UsedTractors ut ON f.ProductID = ut.TractorID
                WHERE f.ProductType = 'UsedTractors'
                AND f.BuyerID = %s
            )
            SELECT 
                fd.*,
                b.BuyerName,
                s.SellerName,
                s.SellerRating
            FROM FavoriteDetails fd
            JOIN Buyers b ON fd.BuyerID = b.BuyerID
            LEFT JOIN Sellers s ON fd.SellerID = s.SellerID
            ORDER BY fd.CreatedAt DESC
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [buyer_id, buyer_id])
            columns = [col[0] for col in cursor.description]
            favorites = [dict(zip(columns, row)) for row in cursor.fetchall()]

            # Process the results
            for favorite in favorites:
                if favorite['ReviewsAndRatings']:
                    try:
                        favorite['ReviewsAndRatings'] = json.loads(favorite['ReviewsAndRatings'])
                    except json.JSONDecodeError:
                        favorite['ReviewsAndRatings'] = None

            # Pagination
            page = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('page_size', 10))
            paginator = Paginator(favorites, page_size)
            current_page = paginator.page(page)

            response_data = {
                'count': paginator.count,
                'total_pages': paginator.num_pages,
                'current_page': page,
                'results': list(current_page.object_list)
            }

            return JsonResponse(response_data, safe=False)

class FavoriteCreateView(APIView):
    @swagger_auto_schema(
        operation_description="Add a product to favorites",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['buyer_id', 'product_type', 'product_id'],
            properties={
                'buyer_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'product_type': openapi.Schema(type=openapi.TYPE_STRING, enum=['Tractors', 'UsedTractors']),
                'product_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            }
        )
    )
    def post(self, request):
        try:
            data = json.loads(request.body)
            buyer_id = data.get('buyer_id')
            product_type = data.get('product_type')
            product_id = data.get('product_id')

            if not all([buyer_id, product_type, product_id]):
                return JsonResponse(
                    {'error': 'All fields are required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            if product_type not in ['Tractors', 'UsedTractors']:
                return JsonResponse(
                    {'error': 'Invalid product type'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            with connection.cursor() as cursor:
                # Check if product exists
                cursor.execute(
                    f"SELECT EXISTS(SELECT 1 FROM {product_type} WHERE TractorID = %s)",
                    [product_id]
                )
                if not cursor.fetchone()[0]:
                    return JsonResponse(
                        {'error': f'No {product_type} found with ID {product_id}'}, 
                        status=status.HTTP_404_NOT_FOUND
                    )

                # Check if already in favorites
                cursor.execute("""
                    SELECT EXISTS(
                        SELECT 1 FROM Favourites 
                        WHERE BuyerID = %s 
                        AND ProductType = %s 
                        AND ProductID = %s
                    )
                """, [buyer_id, product_type, product_id])
                
                if cursor.fetchone()[0]:
                    return JsonResponse(
                        {'error': 'Already in favorites'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Add to favorites
                cursor.execute("""
                    INSERT INTO Favourites (BuyerID, ProductType, ProductID)
                    VALUES (%s, %s, %s)
                    RETURNING FavouriteID, BuyerID, ProductType, ProductID, CreatedAt
                """, [buyer_id, product_type, product_id])

                columns = [col[0] for col in cursor.description]
                result = dict(zip(columns, cursor.fetchone()))

                return JsonResponse(result, status=status.HTTP_201_CREATED)

        except json.JSONDecodeError:
            return JsonResponse(
                {'error': 'Invalid JSON'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return JsonResponse(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class FavoriteDeleteView(APIView):
    @swagger_auto_schema(
        operation_description="Remove a product from favorites",
        responses={204: "No content"}
    )
    def delete(self, request, favorite_id):
        with connection.cursor() as cursor:
            # First get the favorite details for response
            cursor.execute(
                "SELECT * FROM Favourites WHERE FavouriteID = %s",
                [favorite_id]
            )
            favorite = cursor.fetchone()
            
            if not favorite:
                return JsonResponse(
                    {'error': 'Favorite not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            # Delete the favorite
            cursor.execute(
                "DELETE FROM Favourites WHERE FavouriteID = %s",
                [favorite_id]
            )

            return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)

class FavoriteCountView(APIView):
    @swagger_auto_schema(
        operation_description="Get favorite counts for a buyer",
        manual_parameters=[
            openapi.Parameter('buyer_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=True),
        ]
    )
    def get(self, request):
        buyer_id = request.GET.get('buyer_id')
        if not buyer_id:
            return JsonResponse(
                {'error': 'buyer_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        query = """
            SELECT 
                COUNT(*) as total_favorites,
                SUM(CASE WHEN ProductType = 'Tractors' THEN 1 ELSE 0 END) as new_tractors,
                SUM(CASE WHEN ProductType = 'UsedTractors' THEN 1 ELSE 0 END) as used_tractors
            FROM Favourites
            WHERE BuyerID = %s
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [buyer_id])
            columns = [col[0] for col in cursor.description]
            result = dict(zip(columns, cursor.fetchone()))
            
            return JsonResponse(result)