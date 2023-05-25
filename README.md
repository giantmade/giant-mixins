# Giant Mixins

A small, re-usable package which can be used in any project that requires mixins (which is 99% of them)
This will include the standard mixins such as TimestampMixin, PublishingMixin and VideoURLMixin

## Installation

To install the standard app with no extras simply run

    $ poetry add giant-mixins

However if your project has django-cms installed then you can make use of the full range of mixins in this app. For this, install the package with the extra dependencies,

    $ poetry add giant-mixins --extras "cms"

You should then add `"mixins"` to the `INSTALLED_APPS` in your settings file.

## Preparing for release

In order to prep the package for a new release on TestPyPi and PyPi there is one key thing that you need to do. You need to update the version number in the `pyproject.toml`.
This is so that the package can be published without running into version number conflicts. The version numbering must also follow the Semantic Version rules which can be found here https://semver.org/.

## Publishing

Publishing a package with poetry is incredibly easy. Once you have checked that the version number has been updated (not the same as a previous version) then you only need to run two commands.

    $ `poetry build`

will package the project up for you into a way that can be published.

    $ `poetry publish`

will publish the package to PyPi. You will need to enter the company username (Giant-Digital) and password for the account which can be found in the company password manager
