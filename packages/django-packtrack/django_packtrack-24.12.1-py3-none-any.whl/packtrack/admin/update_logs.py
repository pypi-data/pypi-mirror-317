from django.contrib import admin
from packtrack.models import UpdateLog


# Register UpdateLog in the admin
@admin.register(UpdateLog)
class UpdateLogAdmin(admin.ModelAdmin):
    list_display = (
        "package_name",
        "old_version",
        "new_version",
        "update_timestamp",
    )
    search_fields = ("package_name",)
    list_filter = ("update_timestamp",)
    readonly_fields = (
        "package_name",
        "old_version",
        "new_version",
        "console_output",
        "update_timestamp",
    )

    # Disable adding or deleting logs from the admin
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
