from rest_framework import serializers
from .models import OutdatedPackage


class OutdatedPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutdatedPackage
        fields = "__all__"
