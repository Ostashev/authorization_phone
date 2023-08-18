from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CreateUserViewSet, UserProfileViewSet, VerifyCodeViewSet

router = DefaultRouter()
router.register(
    'request_phone_number',
    CreateUserViewSet,
    basename='request_phone_number'
)
router.register('user_profile', UserProfileViewSet, basename='user-profile')
router.register('verify_code', VerifyCodeViewSet, basename='verify_code')

urlpatterns = [
    path('', include(router.urls)),
]
