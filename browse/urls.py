from django.conf.urls.defaults import *
from django.views.generic import list_detail, simple
from django.contrib.admin.models import LogEntry

from models import Usage,KeyWord
RETURNA=Usage.objects.get(pk=2)
REQUESTA=Usage.objects.get(pk=3)
RESTRICTA=Usage.objects.get(pk=1)

urlpatterns = patterns('django.views.generic.list_detail',
    # Example:
    #(r'^browse/', include('dictionary.browse.urls')),
    (r'^$', simple.direct_to_template, {\
        'template':'dictionary/intro.html'} ),
    (r'^restrictables/$', list_detail.object_list, {\
        'queryset':KeyWord.objects.filter(usage=RESTRICTA),
        'template_name':'dictionary/index.html',
        'extra_context':{'firstpara':'Restrictables'}} ),
    (r'^requestables/$', list_detail.object_list, {\
        'queryset':KeyWord.objects.filter(usage=REQUESTA),
        'template_name':'dictionary/index.html',
        'extra_context':{'firstpara':'Requestables'}}),
#    (r'^returnables/$', list_detail.object_list, {\
#        'queryset':KeyWord.objects.filter(usage=RETURNA),
#        'template_name':'dictionary/index.html',
#        'extra_context':{'firstpara':'Returnables'}} ),
    (r'^log/$', list_detail.object_list, {\
        'queryset':LogEntry.objects.all(),
        'template_name':'dictionary/log.html'} ),
)
urlpatterns += patterns('browse.views',
    (r'^returnables/$', 'returnables_by_type'),
    (r'^check/$', 'check'),
    (r'^new/$', 'makenew'),
)
