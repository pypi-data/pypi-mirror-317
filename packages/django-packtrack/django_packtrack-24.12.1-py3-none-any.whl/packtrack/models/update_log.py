from django.db import models


class UpdateLog(models.Model):
    package_name = models.CharField(max_length=255)
    old_version = models.CharField(max_length=50)
    new_version = models.CharField(max_length=50)
    console_output = models.TextField()
    update_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Update Log for {self.package_name} - {self.old_version} to {self.new_version}"
