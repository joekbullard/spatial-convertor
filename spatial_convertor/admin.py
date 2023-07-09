from django.contrib import admin
from .models import SpatialRecord, SpatialLayer

admin.site.register(SpatialRecord)
admin.site.register(SpatialLayer)

# Register your models here.
