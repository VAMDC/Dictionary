from django.conf.urls import patterns, url, include
from django.views.generic.base import TemplateView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='dictionary/intro.html')),
    )
urlpatterns += patterns('browse.views',
    (r'^returnables/$', 'returnables_by_type'),
    (r'^restrictables/$', 'restrictables'),
    (r'^requestables/$', 'requestables'),
    (r'^log/$', 'log'),
    (r'^check/$', 'check'),
    (r'^new/$', 'makenew'),
)
