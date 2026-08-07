#!/usr/bin/env python3
import re, os, sys

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from browse.models import KeyWord, Usage

# path to the vamdctap checkout whose generators.py is compared against
GENERATORS = os.environ.get('VAMDCTAP_GENERATORS', '../vamdctap/generators.py')

def flatten(l, ltypes=(list, tuple)):
    ltype = type(l)
    l = list(l)
    i = 0
    while i < len(l):
        while isinstance(l[i], ltypes):
            if not l[i]:
                l.pop(i)
                i -= 1
                break
            else:
                l[i:i + 1] = l[i]
        i += 1
    return ltype(l)

reg = re.compile(r'G\([\'"][a-zA-Z0-9]*[\'"]\)')
gen = open(GENERATORS).readlines()
gen = [reg.findall(l) for l in gen]
gen = flatten(gen)
gen = [g for g in gen if 'LOG(' not in g]
gen = [l[3:-2] for l in gen]

implkws = [g.lower() for g in gen]
########################
for kw in gen:
    try: k=KeyWord.objects.get(name__iexact=kw)
    except KeyWord.DoesNotExist: print('Not in dictionary: %s'%kw)

reg = re.compile(r'makeDataType\([\'"][a-zA-Z0-9]*[\'"],\s*[\'"][a-zA-Z0-9]*[\'"]')
gen = open(GENERATORS).readlines()
gen = [reg.findall(l) for l in gen]
gen = flatten(gen)
gen = [l.split("'")[3] for l in gen]

for kw in gen:
    try: k=KeyWord.objects.get(name__iexact=kw)
    except KeyWord.DoesNotExist:
        print('Not in dictionary: %s'%kw)
        continue
    if not k.datatype:
        print('Not a DataType: %s'%kw)

implkws += [g.lower() for g in gen]
########
returnable = Usage.objects.get(name__iexact='returnable')
for kw in returnable.keyword_set.iterator():
    if kw.name.lower() not in implkws:
        print('Unimplemented Returnable: %s'%kw)
