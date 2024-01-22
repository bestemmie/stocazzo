from django.urls import path, include
from .views import *

urlpatterns = [
    path('', homepage),
    path('trucchi', trucchi),
    path('ss', ss),
    path('staff', staff),
    path('bestclicker', best_buildform),
    path('bestclicker/download', best_download, name="best-dl"),
]
