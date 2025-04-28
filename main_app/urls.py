from django.urls import path
from . import views # Import views to connect routes to view functions

urlpatterns = [
    # Routes will be added here
    path('', views.home, name='home'),
    path('plants/', views.plant_index, name='plant-index'),
    path('plants/<int:plant_id>/', views.plant_detail, name='plant-detail'), # can change the link address
    path('plants/create/', views.PlantCreate.as_view(), name='plant-create'),
]