from django.db import models
from hydroponic_system.models import HydroponicSystem


class Measurements(models.Model):
    hydroponic_system = models.ForeignKey(HydroponicSystem,
                                          on_delete=models.CASCADE,
                                          related_name="measurements")
    ph = models.FloatField()
    water_temperature = models.FloatField()
    tds = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
