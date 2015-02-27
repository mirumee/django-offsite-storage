from __future__ import unicode_literals

from django.contrib.staticfiles.management.commands import collectstatic

from ... import settings


class Command(collectstatic.Command):

    def set_options(self, **options):
        super(Command, self).set_options(**options)
        self.ignore_patterns += settings.IGNORE_FILES
