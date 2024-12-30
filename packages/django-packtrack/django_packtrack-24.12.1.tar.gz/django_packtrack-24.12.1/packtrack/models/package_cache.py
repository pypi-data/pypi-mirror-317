from django.db import models


class PackageCache(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Package name
    latest_version = models.CharField(max_length=50)  # Latest version from PyPI
    last_checked = models.DateTimeField()  # Timestamp of when it was last checked

    def __str__(self):
        return (
            f"{self.name} - {self.latest_version} (Last checked: {self.last_checked})"
        )
