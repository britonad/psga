from django.urls import path
from app.api import views

# Django URL conf used instead of the DRF router for the sake of simplicity.
urlpatterns = [
    path(
        'positions/<int:imo>/',
        views.ListShipPositionsView.as_view(),
        name='ship_positions'
    ),
    path('ships/', views.ListShipsView.as_view(), name='ships'),
]
