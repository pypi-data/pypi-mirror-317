from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'taskresults', views.TaskResultViewSet)
router.register(r'groupresults', views.GroupResultViewSet)

urlpatterns = [
    path('', include(router.urls))
]
