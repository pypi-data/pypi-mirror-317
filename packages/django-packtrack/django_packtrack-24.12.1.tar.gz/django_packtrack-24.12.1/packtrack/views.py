from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import OutdatedPackage

from oauth2_provider.contrib.rest_framework import OAuth2Authentication, TokenHasScope


class OutdatedPackagesListView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ["read"]  # Ensure that the correct scope is set here

    def get(self, request):
        packages = OutdatedPackage.objects.all()
        data = [
            {
                "name": package.name,
                "installed_version": package.installed_version,
                "latest_version": package.latest_version,
                "last_checked": package.last_checked,
                "dependent_apps": package.dependent_apps,
            }
            for package in packages
        ]
        return Response(data)
