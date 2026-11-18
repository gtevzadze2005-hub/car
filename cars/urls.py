from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_car, name='add_car'),
    path('', views.car_list, name='car_list'),
    path('<int:car_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('<int:car_id>/edit/',views.edit_car,name='edit_car'),
    path('<int:car_id>/delete/',views.delete_car,name='delete_car'),
    path('<int:car_id>/', views.car_detail, name='car_detail'),
]