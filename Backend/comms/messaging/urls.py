from django.urls import path
from . import views

urlpatterns = [
    path('conversations/', views.MessagingViewSet.as_view({
        'get': 'list',
        # 'post': 'create_conversation'
    })),
    path('chat/', views.MessagingViewSet.as_view({
        # 'get': 'list',
        'post': 'create_conversation'
    })),
    path('conversations/<int:pk>/', views.MessagingViewSet.as_view({
        'get': 'retrieve'
    })),
    path('conversations/<int:pk>/mark-read/', views.MessagingViewSet.as_view({
        'post': 'mark_read'
    })),
    path('messages/send/', views.SendMessageView.as_view(), name='send-message'),

]