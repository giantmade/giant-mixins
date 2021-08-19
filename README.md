# Giant Mixins

A small, re-usable package which can be used in any project that requires mixins (which is 99% of them)
This will include the standard mixins such as TimestampMixin, PublishingMixin and VideoURLMixin

## Installation

To install the standard app with no extras simply run

    $ poetry add giant-mixins

However if your project has django-cms installed then you can make use of the full range of mixins in this app. For this, install the package with the extra dependencies,

    $ poetry add giant-mixins --extras "cms"

You should then add `"mixins"` to the `INSTALLED_APPS` in your settings file.
