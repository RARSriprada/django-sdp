from django.contrib import admin
from django.urls import path, include  # include is required to include app-specific urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pro.urls')),  # Include your app's urls
]
