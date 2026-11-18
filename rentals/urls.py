from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:car_id>/',views.book_car, name='book_car'),
    path('manage/<int:rental_id>/<str:action>/',views.manage_rental,name='manage_rental'),
    path('cancel/<int:rental_id>/',views.cancel_rental,name='cancel_rental'),
    path('payment/', views.payment_page, name='payment_page'),
    path('complete/<int:rental_id>/',views.complete_rental,name='complete_rental'),
]
