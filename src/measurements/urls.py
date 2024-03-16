from django.urls import path

from measurements.views import HydroponicSystemMeasurementsListCreate, Last10MeasurementsList # noqa

urlpatterns = [
    path('<int:system_id>/', HydroponicSystemMeasurementsListCreate.as_view(),
         name='system_measurements'),
    path('<int:system_id>/last10/', Last10MeasurementsList.as_view(),
         name='last_10_measurements'),
]
