from django.urls import include, path
from rest_framework import routers
from fleet import views


router = routers.DefaultRouter()

router.register(r'aircraft', views.AircraftViewset, basename="aircraft")
router.register(r'airport', views.AirportViewset, basename='airport')
router.register(r'flight', views.FlightViewset, basename="flight")

urlpatterns = [
    path('', include(router.urls))
]