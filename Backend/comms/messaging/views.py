from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.db import connection
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView


class MessagingViewSet(ViewSet):
    def dictfetchall(self, cursor):
        """Return all rows from a cursor as a list of dictionaries"""
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    def dictfetchone(self, cursor):
        """Return one row from a cursor as a dictionary"""
        if cursor.description is None:
            return None
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        if row is None:
            return None
        return dict(zip(columns, row))

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'user_type', 
                openapi.IN_QUERY,
                description="Type of user (BUYER or SELLER)",
                type=openapi.TYPE_STRING,
                required=True,
                enum=['BUYER', 'SELLER']
            ),
            openapi.Parameter(
                'user_id', 
                openapi.IN_QUERY,
                description="ID of the user",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="List of conversations",
                examples={
                    "application/json": [{
                        "conversation_id": 1,
                        "seller_username": "string",
                        "seller_company": "string",
                        "unread_count": 0,
                        "latest_message": {
                            "content": "string",
                            "timestamp": "2024-01-01T00:00:00Z",
                            "sender_type": "string"
                        }
                    }]
                }
            )
        }
    )
    def list(self, request):
        user_type = request.query_params.get('user_type')
        user_id = request.query_params.get('user_id')
        
        with connection.cursor() as cursor:
            if user_type == 'BUYER':
                cursor.execute("""
                    SELECT 
                        c.conversation_id,
                        c.BuyerID,
                        c.SellerID,
                        c.created_at,
                        c.updated_at,
                        s.username as seller_username,
                        s.CompanyDetails as seller_company,
                        COUNT(CASE WHEN m.is_read = FALSE AND m.sender_type != 'BUYER' THEN 1 END) as unread_count,
                        (
                            SELECT JSON_OBJECT(
                                'content', content,
                                'timestamp', timestamp,
                                'sender_type', sender_type
                            )
                            FROM Messages 
                            WHERE conversation_id = c.conversation_id 
                            ORDER BY timestamp DESC 
                            LIMIT 1
                        ) as latest_message
                    FROM Conversations c
                    JOIN Sellers s ON c.SellerID = s.SellerID
                    LEFT JOIN Messages m ON c.conversation_id = m.conversation_id
                    WHERE c.BuyerID = %s
                    GROUP BY c.conversation_id, c.BuyerID, c.SellerID, c.created_at, c.updated_at, 
                             s.username, s.CompanyDetails
                    ORDER BY c.updated_at DESC
                """, [user_id])
            else:
                cursor.execute("""
                    SELECT 
                        c.conversation_id,
                        c.BuyerID,
                        c.SellerID,
                        c.created_at,
                        c.updated_at,
                        b.username as buyer_username,
                        COUNT(CASE WHEN m.is_read = FALSE AND m.sender_type != 'SELLER' THEN 1 END) as unread_count,
                        (
                            SELECT JSON_OBJECT(
                                'content', content,
                                'timestamp', timestamp,
                                'sender_type', sender_type
                            )
                            FROM Messages 
                            WHERE conversation_id = c.conversation_id 
                            ORDER BY timestamp DESC 
                            LIMIT 1
                        ) as latest_message
                    FROM Conversations c
                    JOIN Buyers b ON c.BuyerID = b.BuyerID
                    LEFT JOIN Messages m ON c.conversation_id = m.conversation_id
                    WHERE c.SellerID = %s
                    GROUP BY c.conversation_id, c.BuyerID, c.SellerID, c.created_at, c.updated_at, 
                             b.username
                    ORDER BY c.updated_at DESC
                """, [user_id])
            
            conversations = self.dictfetchall(cursor)
            return Response(conversations)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'pk', 
                openapi.IN_PATH,
                description="Conversation ID",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Detailed conversation with messages",
                examples={
                    "application/json": {
                        "conversation_id": 1,
                        "buyer_username": "string",
                        "seller_username": "string",
                        "seller_company": "string",
                        "messages": [{
                            "id": 1,
                            "content": "string",
                            "sender_type": "string",
                            "sender_id": 1,
                            "timestamp": "2024-01-01T00:00:00Z",
                            "is_read": True
                        }]
                    }
                }
            ),
            404: openapi.Response(description="Conversation not found")
        }
    )
    def retrieve(self, request, pk=None):
        with connection.cursor() as cursor:
            # Get conversation details
            cursor.execute("""
                SELECT 
                    c.conversation_id,
                    c.BuyerID,
                    c.SellerID,
                    c.created_at,
                    c.updated_at,
                    b.username as buyer_username,
                    s.username as seller_username,
                    s.CompanyDetails as seller_company
                FROM Conversations c
                JOIN Buyers b ON c.BuyerID = b.BuyerID
                JOIN Sellers s ON c.SellerID = s.SellerID
                WHERE c.conversation_id = %s
            """, [pk])
            
            conversation = self.dictfetchone(cursor)
            
            if not conversation:
                return Response({'error': 'Conversation not found'}, status=404)
            
            # Get messages
            cursor.execute("""
                SELECT 
                    Message_id as id,
                    content,
                    sender_type,
                    sender_id,
                    timestamp,
                    is_read
                FROM Messages
                WHERE conversation_id = %s
                ORDER BY timestamp ASC
            """, [pk])
            
            messages = self.dictfetchall(cursor)
            conversation['messages'] = messages
            
            return Response(conversation)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['buyer_id', 'seller_id'],
            properties={
                'buyer_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'seller_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            }
        ),
        responses={
            201: openapi.Response(
                description="Conversation created",
                examples={
                    "application/json": {
                        "conversation_id": 1
                    }
                }
            ),
            200: openapi.Response(
                description="Existing conversation found",
                examples={
                    "application/json": {
                        "conversation_id": 1
                    }
                }
            )
        }
    )
    @action(detail=False, methods=['post'])
    def create_conversation(self, request):
        buyer_id = request.data.get('buyer_id')
        seller_id = request.data.get('seller_id')
        
        with connection.cursor() as cursor:
            # Check if conversation already exists
            cursor.execute("""
                SELECT conversation_id 
                FROM Conversations
                WHERE BuyerID = %s AND SellerID = %s
            """, [buyer_id, seller_id])
            
            existing = cursor.fetchone()
            if existing:
                return Response({'conversation_id': existing[0]})
            
            # Create new conversation
            cursor.execute("""
                INSERT INTO Conversations (BuyerID, SellerID, created_at, updated_at)
                VALUES (%s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            """, [buyer_id, seller_id])
            
            conversation_id = cursor.lastrowid
            connection.commit()
            
            
            return Response({'conversation_id': conversation_id}, status=201)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['user_type', 'user_id'],
            properties={
                'user_type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['BUYER', 'SELLER']
                ),
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            }
        ),
        responses={
            200: openapi.Response(
                description="Messages marked as read",
                examples={
                    "application/json": {
                        "status": "messages marked as read"
                    }
                }
            )
        }
    )
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        user_type = request.data.get('user_type')
        user_id = request.data.get('user_id')
        
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE Messages
                SET is_read = TRUE
                WHERE conversation_id = %s
                AND sender_type != %s
                AND is_read = FALSE
            """, [pk, user_type])
            
            connection.commit()
            return Response({'status': 'messages marked as read'})
        



class SendMessageView(APIView):

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'conversation_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the conversation", example=1),
                'content': openapi.Schema(type=openapi.TYPE_STRING, description="Content of the message", example="How much is the tractor?"),
                'sender_type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Type of the sender (BUYER or SELLER)",
                    enum=['BUYER', 'SELLER'],
                    example='BUYER'
                ),
                'sender_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the sender", example=101),
                'reply_to_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the message being replied to (optional)", example=None)
            },
            required=['conversation_id', 'content', 'sender_type', 'sender_id']  # Required fields
        ),
        responses={
            200: openapi.Response(
                description="Message sent successfully",
                examples={
                    "application/json": {
                        "message_id": 1
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request, missing required fields",
                examples={
                    "application/json": {
                        "error": "Missing required fields"
                    }
                }
            )
        }
    )
    def post(self, request):
        conversation_id = request.data.get('conversation_id')
        content = request.data.get('content')
        sender_type = request.data.get('sender_type')
        sender_id = request.data.get('sender_id')
        reply_to_id = request.data.get('reply_to_id')  # Optional for replies

        if not all([conversation_id, content, sender_type, sender_id]):
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        with connection.cursor() as cursor:
            # Insert the new message
            cursor.execute("""
                INSERT INTO Messages (conversation_id, content, sender_type, sender_id, reply_to_id, timestamp)
                VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            """, [conversation_id, content, sender_type, sender_id, reply_to_id])

            message_id = cursor.lastrowid
            connection.commit()

        return Response({'message_id': message_id}, status=status.HTTP_201_CREATED)
