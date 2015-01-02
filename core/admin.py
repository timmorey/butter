from django.contrib import admin

from butter.core.models import Dialect, Resource, Unit

admin.site.register(Dialect)
admin.site.register(Resource)
admin.site.register(Unit)

