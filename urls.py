from django.urls import path, include

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    path('', include('browse.urls')),
    path('admin/', admin.site.urls),
]
