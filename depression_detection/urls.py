from django.urls import path
from . import views
from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('', views.process_form, name='process_form'),  # Define URL pattern for process_form view
    path('admin/', admin.site.urls),
    
]


# urlpatterns = [
#     path('', include('members.urls')),
# ]