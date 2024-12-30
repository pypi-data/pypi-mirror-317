from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.urls import reverse
from django.core.management import call_command
from packtrack.models import OutdatedPackage, PackageCache, UpdateLog
from django.db import models
from packtrack.utils import update_outdated_packages_list


# Custom filter to show/hide packages where installed_version equals latest_version
class VersionMatchFilter(admin.SimpleListFilter):
    title = "version match"  # Title of the filter
    parameter_name = "version_match"  # Query parameter name

    def lookups(self, request, model_admin):
        return (
            ("yes", "Installed == Latest"),
            ("no", "Installed != Latest"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(installed_version=models.F("latest_version"))
        if self.value() == "no":
            return queryset.exclude(installed_version=models.F("latest_version"))
        return queryset


@admin.register(OutdatedPackage)
class OutdatedPackageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "installed_version",
        "latest_version",
        "last_checked",
        "dependent_apps",
        "update_package_button",  # Add the custom button to list display
    )
    list_filter = ("last_checked", VersionMatchFilter)  # Add custom filter
    search_fields = ("name", "dependent_apps")

    # Add custom button
    change_list_template = "packtrack/admin/outdated_packages_change_list.html"

    # Custom action to update all outdated packages
    def update_packages(self, request):
        update_outdated_packages_list()
        self.message_user(request, "Outdated packages updated successfully.")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    # Custom button to trigger package update
    def update_package_button(self, obj):
        return format_html(
            '<a class="button" href="{}">Update</a>',
            reverse("admin:update-single-package", args=[obj.pk]),
        )

    update_package_button.short_description = "Update Package"
    update_package_button.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "update-packages/",
                self.admin_site.admin_view(self.update_packages),
                name="update-packages",
            ),
            path(
                "update-package/<int:package_id>/",
                self.admin_site.admin_view(self.update_single_package),
                name="update-single-package",
            ),
        ]
        return custom_urls + urls

    def update_single_package(self, request, package_id):
        # Fetch the package from the database
        try:
            package = OutdatedPackage.objects.get(pk=package_id)
        except OutdatedPackage.DoesNotExist:
            self.message_user(
                request, f"Package with id {package_id} not found.", level="error"
            )
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        # Call the management command to update the specific package
        try:
            call_command("update_package", package.name)
            self.message_user(
                request, f"Package '{package.name}' updated to the latest version."
            )
        except Exception as e:
            self.message_user(
                request,
                f"Error updating package '{package.name}': {str(e)}",
                level="error",
            )

        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
