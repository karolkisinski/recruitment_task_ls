from django.contrib import admin

# Register your models here.

from hydroponic_system.models import HydroponicSystem
from measurements.models import Measurements
admin.site.register(HydroponicSystem)
admin.site.register(Measurements)
