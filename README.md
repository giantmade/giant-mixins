# Giant Mixins

A small, re-usable package which can be used in any project that requires mixins (which is 99% of them)
This will include the standard mixins such as TimestampMixin, PublishingMixin and VideoURLMixin

## Installation

To install the standard app with no extras simply run

    $ poetry add giant-mixins

However if your project has django-cms installed then you can make use of the full range of mixins in this app. For this, install the package with the extra dependencies,

    $ poetry add giant-mixins --extras "cms"

You should then add `"mixins"` to the `INSTALLED_APPS` in your settings file.

## Usage

The mixins are a collection of classes that can be implemented into various files of your django project. Simply add the mixin class name as an argument to your chosen project class.

### AbstractExportMixin

The purpose of this mixin is to allow your project app to be able to easily prepare model data for an export to csv method (or similar export method).
* To write out your header row, call get_fieldnames_for_export upon the first row of your queryset.

    
    writer.writerow(queryset.first().get_fieldnames_for_export)

* To write out values for those fields listed in the header row call prepare_csv_export_data:


    for obj in queryset:
        writer.writerow(obj.prepare_csv_export_data)

* If you don't wish to export all of the fields in your model then overwrite the prepare_csv_export_fields property.

### SearchIndexMixin

The purpose of this mixin is to allow the project app to implement the key SearchIndex API methods from Haystack.
