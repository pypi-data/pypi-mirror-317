from django.db import models


class OutdatedPackage(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Package name
    installed_version = models.CharField(max_length=50)  # Installed version
    latest_version = models.CharField(max_length=50)  # Latest version from PyPI
    last_checked = models.DateTimeField()  # Timestamp of when it was last checked
    dependent_apps = models.TextField(
        blank=True
    )  # Dependent packages or apps (comma-separated)

    def __str__(self):
        return f"{self.name} (Installed: {self.installed_version}, Latest: {self.latest_version})"
