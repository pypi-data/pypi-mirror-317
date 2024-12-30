from django.urls import path, include
from .views import OutdatedPackagesListView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path(
        "api/outdated-packages/",
        OutdatedPackagesListView.as_view(),
    ),
    path("o/", include("oauth2_provider.urls", namespace="oauth2_provider")),
]

urlpatterns += [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
