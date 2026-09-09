from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

from .views import (
    MemberViewSet, MembershipPlanViewSet, SubscriptionViewSet,
    AttendanceViewSet, PaymentViewSet, TrainerViewSet, WorkoutPlanViewSet,
    DashboardStatsAPIView
)

router = DefaultRouter()
router.register(r'members', MemberViewSet, basename='member')
router.register(r'membership-plans', MembershipPlanViewSet, basename='membership-plan')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')
router.register(r'attendance', AttendanceViewSet, basename='attendance')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'trainers', TrainerViewSet, basename='trainer')
router.register(r'workouts', WorkoutPlanViewSet, basename='workout')

urlpatterns = [
    # Auth Endpoints
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair_alias'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh_alias'),
    path('auth/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),

    # Dashboard Stats Endpoint
    path('dashboard/stats/', DashboardStatsAPIView.as_view(), name='dashboard_stats'),

    # Router endpoints
    path('', include(router.urls)),
]
