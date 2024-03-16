from django.urls import path
from .views import HydroponicSystemListCreate, HydroponicSystemRetrieveUpdateDestroy # noqa


urlpatterns = [
    path('', HydroponicSystemListCreate.as_view(),
         name='hydroponic-systems'),
    path('<int:pk>/', HydroponicSystemRetrieveUpdateDestroy.as_view(),
         name='hydroponic-system-api')
]
