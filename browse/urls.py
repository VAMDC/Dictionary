from django.urls import path, re_path, include
from django.views.generic.base import TemplateView

from .views import *

urlpatterns = [
    path('', TemplateView.as_view(template_name='browse/intro.html')),
    path('returnables/', returnables_by_type),
    path('restrictables/', restrictables),
    path('requestables/', requestables),
    path('log/', log),
    path('check/', check),
    path('new/', makenew),
]
