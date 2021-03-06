#!/usr/bin/env python2

import django, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

from django.db.models import Q
from browse.models import KeyWord, Usage
RESTR = Usage.objects.get(name='Restrictable')

noMeth = ~Q(name__endswith='Method')
noRef = ~Q(name__endswith='Ref')
ks = KeyWord.objects.filter(sdescr='.')
print ks.count()

for k in ks:
    print k.name, k.sdescr, k.ldescr
    sdescr=raw_input('New sdescr: ')
    if not sdescr: continue
    k.sdescr = sdescr
    if k.ldescr == '.':
        k.ldescr = sdescr
    k.save()
    print k.name, k.sdescr, k.ldescr

