import csv

from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone
from django.utils.text import slugify


class CSVAdminMixin(admin.ModelAdmin):
    """
    Allows us to add a csv exporter to admins
    """

    def get_actions(self, request):
        actions = self.actions if hasattr(self, "actions") else []
        actions.append("csv_export")
        actions = super().get_actions(request)
        return actions

    def export_csv(self, request, queryset):
        """
        CSV exporter
        """
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="{name}-{date}.csv"'.format(
            date=timezone.now().date(), name=slugify(queryset.model._meta.verbose_name_plural)
        )

        writer = csv.writer(response)

        # Build the headers based on the first object in the queryset
        writer.writerow(queryset.first().get_fieldnames_for_export)

        for obj in queryset:
            writer.writerow(obj.prepare_csv_export_data)

        return response

    export_csv.short_description = "Export selected as CSV"
