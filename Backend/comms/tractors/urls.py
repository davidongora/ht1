from django.urls import path
from .views import TractorsListCreateView,TractorDetailView,SearchTractors

urlpatterns = [
    path('tractors/', TractorsListCreateView.as_view(), name='tractor-list-create'),
    path('tractors/<int:pk>/', TractorDetailView.as_view(), name='tractor-detail'),
    path('tractors/search/', SearchTractors.as_view(), name='tractor-search'),
]