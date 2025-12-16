from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserViewSet, SectionViewSet, MaterialViewSet,
    TestViewSet, TestResultViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'sections', SectionViewSet, basename='section')
router.register(r'materials', MaterialViewSet, basename='material')
router.register(r'tests', TestViewSet, basename='test')
router.register(r'test-results', TestResultViewSet, basename='test-result')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
