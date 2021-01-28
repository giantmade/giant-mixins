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

    def get_export_fields(self, request):
        """
        Build a list of model fields to add to the csv
        """
        model_fields = self.get_form(request, obj=self).Meta.fields
        if hasattr(self, "csv_fields"):
            return self.csv_fields
        elif hasattr(self, "csv_excluded_fields"):
            return [
                field for field in model_fields if field not in self.csv_excluded_fields
            ]
        else:
            return model_fields

    def csv_export(self, request, queryset=None, *args, **kwargs):
        """
        Generic csv export admin action.
        """
        fields = self.get_export_fields(request)
        model_name = slugify(self.model._meta.verbose_name_plural)
        date = timezone.now().date()

        response = HttpResponse(content_type="text/csv")
        response[
            "Content-Disposition"
        ] = f"attachment; filename={model_name}-{date}.csv"
        writer = csv.writer(response)

        # Build a list of headers for the csv
        header_names = [field.title() for field in fields]
        field_names = [field for field in fields]
        # Write a first row with header information
        writer.writerow(header_names)
        # Write data rows
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        return response

    csv_export.short_description = "Exported selected to CSV"
