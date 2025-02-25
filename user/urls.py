from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import (
    RegisterView,
    ProfileView,
    AddressCreateReadView,
    AddressUpdateDeleteView,
    ChangePasswordView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/', RegisterView.as_view()),
    path('<int:user_id>/password/', ChangePasswordView.as_view()),
    path('<int:user_id>/profile/', ProfileView.as_view()),
    path('<int:user_id>/address/', AddressCreateReadView.as_view()),
    path('<int:user_id>/address/<int:address_id>/', AddressUpdateDeleteView.as_view()),
]
