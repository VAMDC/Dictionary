#!/usr/bin/env python3

import django, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

from django.db.models import Q
from browse.models import KeyWord
noMeth = ~Q(name__endswith='Method')
noRef = ~Q(name__endswith='Ref')
ks = KeyWord.objects.filter(sdescr='.')
print(ks.count())

for k in ks:
    print(k.name, k.sdescr, k.ldescr)
    sdescr=input('New sdescr: ')
    if not sdescr: continue
    k.sdescr = sdescr
    if k.ldescr == '.':
        k.ldescr = sdescr
    k.save()
    print(k.name, k.sdescr, k.ldescr)

