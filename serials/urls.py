from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SerialViewSet, get_serials_values, get_serials_row, get_serials_paginated, get_serials_threaded

router = DefaultRouter()
router.register(r'serials', SerialViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('values/', get_serials_values, name='serial-values'),
    path('row/', get_serials_row, name='serial-row'),
    path('paginated/', get_serials_paginated, name='serial-paginated'),
   # path('parallel/', get_serials_parallel, name='serial-parallel'),
    path('threaded/', get_serials_threaded, name='serial-threaded'),
]