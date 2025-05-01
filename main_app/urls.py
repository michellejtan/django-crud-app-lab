from django.urls import path
from . import views # Import views to connect routes to view functions

urlpatterns = [
    # Routes will be added here
    path('', views.home, name='home'),
    path('plants/', views.plant_index, name='plant-index'),
    path('plants/<int:plant_id>/', views.plant_detail, name='plant-detail'), # can change the link address
    path('plants/create/', views.PlantCreate.as_view(), name='plant-create'),
    path('plants/<int:pk>/update/', views.PlantUpdate.as_view(), name='plant-update'),
    path('plants/<int:pk>/delete/', views.PlantDelete.as_view(), name='plant-delete'),
    path(
        'plants/<int:plant_id>/add-care/', 
        views.add_care, 
        name='add-care'
    ),
    path('supplies/create/', views.SupplyCreate.as_view(), name='supply-create'),
    path('supplies/<int:pk>/', views.SupplyDetail.as_view(), name='supply-detail'),
    path('supplies/', views.SupplyList.as_view(), name='supply-index'),

    path('supplies/<int:pk>/update/', views.SupplyUpdate.as_view(), name='supply-update'),
    path('supplies/<int:pk>/delete/', views.SupplyDelete.as_view(), name='supply-delete'),

    # to associate a plant with a supply
    path('plants/<int:plant_id>/associate-supply/<int:supply_id>/', views.associate_supply, name='associate-supply'),
    path('plants/<int:plant_id>/remove-supply/<int:supply_id>/', views.remove_supply, name='remove-supply'),
]