from django.contrib import admin

from .models import Feature, Statistics, Mesh, Scatter


admin.site.register(Feature)
admin.site.register(Statistics)
admin.site.register(Mesh)
admin.site.register(Scatter)