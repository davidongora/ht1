from django.urls import path
from .views import ImplementListCreateView, ImplementDetailView, ImplementSearchView

urlpatterns = [
    path('implements/', ImplementListCreateView.as_view(), name='implement-list-create'),
    path('implements/<int:implement_id>/', ImplementDetailView.as_view(), name='implement-detail'),
    path('implements/search/', ImplementSearchView.as_view(),  name='implement-detail')
    
]