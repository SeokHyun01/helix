from rest_framework.routers import DefaultRouter
from django.urls import (
    path,
    include,
)

from event import views


router = DefaultRouter()
router.register('events', views.EventViewSet, basename='events')

app_name = 'event'

urlpatterns = [
    path('', include(router.urls)),
]
