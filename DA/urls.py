from django.contrib import admin
from django.urls import path, include
# from . import view
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('depression_detection/', permanent=False)),
    path('depression_detection/', include('depression_detection.urls')),  # Include URL patterns from depression_detection app
]