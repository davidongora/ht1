from django.urls import path
from .views import UsedTractorsListCreateView,UsedTractorDetailView,SearchUsedTractors

urlpatterns = [
    path('used-tractors/', UsedTractorsListCreateView.as_view(), name='tractor-list-create'),
    path('used-tractors/<int:pk>/', UsedTractorDetailView.as_view(), name='tractor-detail'),
    path('used-tractors/search/', SearchUsedTractors.as_view(), name='tractor-favorite'),
]