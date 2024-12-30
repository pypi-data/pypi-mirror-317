from django.contrib import admin
from packtrack.models import PackageCache


@admin.register(PackageCache)
class PackageCacheAdmin(admin.ModelAdmin):
    list_display = ("name", "latest_version", "last_checked")  # Fields to display
    search_fields = ("name",)  # Search by name
    list_filter = ("last_checked",)  # Filter by last checked time
    readonly_fields = ("name", "latest_version", "last_checked")  # Read-only fields

    def has_add_permission(self, request):
        return False  # Disable manual addition of cache entries

    def has_delete_permission(self, request, obj=None):
        return False  # Disable manual deletion of cache entries
