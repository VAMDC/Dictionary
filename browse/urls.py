from django.urls import path, re_path, include
from django.views.generic.base import TemplateView

from .views import *

urlpatterns = [
    path('', TemplateView.as_view(template_name='browse/intro.html')),
    re_path(r'returnables/?$', returnables_by_type),
    re_path(r'restrictables/?$', restrictables),
    re_path(r'requestables/?$', requestables),
    re_path(r'log/?$', log),
    re_path(r'check/?$', check),
    re_path(r'new/?$', makenew),
]
