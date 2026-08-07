# Create your views here.
import ast

from django import forms
from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms.models import modelformset_factory
from django.http import HttpResponse
from django.contrib.admin.models import LogEntry


from .models import KeyWord

RETURNABLE = 'Returnable'
REQUESTABLE = 'Requestable'
RESTRICTABLE = 'Restrictable'

import re
REGEX1=re.compile(r"""^\s*(RETURNABLES|RESTRICTABLES)\s*=\s*\{\s*\\?\s*(['"]\w+['"]\s*:\s*[ru]?['"][\w\-\\_\.,/()\[\]'"=\ ]*['"]\s*,?\s*)*\s*\}\s*$""")

REGEX2=re.compile(r"""^(Atom|AtomState|Source|Molecule|MoleculeState|CollTran|RadTran|Method|MoleQNs)\..*$""")

def log(request):
    logs = LogEntry.objects.all()
    return render(request,'browse/log.html',{'object_list':logs})

def restrictables(request):
    words = KeyWord.objects.filter(usage__name=RESTRICTABLE)
    return render(request,'browse/index.html',{'firstpara':'Restrictables','object_list':words})

def requestables(request):
    words = KeyWord.objects.filter(usage__name=REQUESTABLE)
    return render(request,'browse/index.html',{'firstpara':'Requestables','object_list':words})

def returnables_by_type(request):
    RetQ = Q(usage__name=RETURNABLE)
    atoms = KeyWord.objects.filter(RetQ, block__in=('at','as'))
    atoms.desc = 'Atoms and atomic states'
    atoms.tag = 'at'
    molecs = KeyWord.objects.filter(RetQ, block__in=('mo','ms','mq'))
    molecs.desc = 'Molecules, their states and quantum numbers'
    molecs.tag = 'mo'
    solp= KeyWord.objects.filter(RetQ, block__in=('sd','pa'))
    solp.desc = 'Solids and Particles'
    solp.tag = 'sp'
    procs = KeyWord.objects.filter(RetQ, block__in=('rt','ct','nr'))
    procs.desc = 'Processes'
    procs.tag = 'pr'
    oth = KeyWord.objects.filter(RetQ, block__in=('en','fu','me','so'))
    oth.desc = 'Environments, Functions, Methods and Sources'
    oth.tag = 'oh'
    noxsams = KeyWord.objects.filter(RetQ, block=None)
    noxsams.desc = 'Unclassified Keywords'
    noxsams.tag = 'nx'
    blocs = [atoms, molecs, solp, procs, oth, noxsams]
    return render(request, 'browse/bytype.html', {'blocs': blocs})

def bareKW(kw):
    kw = kw.lower()
    suffixes=['unit','ref','comment','accuracy','method']
    for suff in suffixes:
        if kw.endswith(suff):
            return kw.rsplit(suff,1)[0]

def check_keyword_exists(kw):
    try: KeyWord.objects.get(name__iexact=kw)
    except KeyWord.DoesNotExist:
        barekw = bareKW(kw)
        if not barekw:
            return 'Keyword %s does not exist in the dictionary.'%kw

        try: k = KeyWord.objects.get(name__iexact=barekw)
        except KeyWord.DoesNotExist:
            return 'Keyword %s does not exist in the dictionary. (It is used with one of the DataType suffixes)'%barekw
        if not k.datatype:
            return 'Your used keyword %s with a DataType suffix but it is not a DataType.'%barekw

def check_keyword_usage(kw,usage):
    try: kw = KeyWord.objects.get(name__iexact=kw)
    except KeyWord.DoesNotExist: return
    if not kw.usage.filter(name=usage).exists():
        return '%s is not a %s according to the dictionary.'%(kw,usage)

def check_returnvalues(kw,value):
    if not REGEX2.match(value):
        return 'The value "%s" of %s does not start with one of the known prefixes. This is fine, if you intend to return this as a constant string.'%(value,kw)

def check_unit(kw,keys):
    try: k = KeyWord.objects.get(name__iexact=kw)
    except KeyWord.DoesNotExist: return
    if k.datatype:
        keys = [key.lower() for key in keys]
        if not kw.lower() + 'unit' in keys:
            return 'You use the DataType %s but not the corresponding keyword for its unit (%sUnit).'%(kw,kw)

def validate_dict(data):
    errors=[]
    if not REGEX1.match(data):
        errors.append('First syntax check did not pass. (Comments with # are not allowed in this check.)')

    if '=' not in data:
        errors.append('Neither RETURNABLES or RESTRICTABLES assignment found')
        raise ValidationError(errors)

    name,value = data.split('=',1)
    name=name.strip()
    if name == 'RETURNABLES': usage = RETURNABLE
    elif name == 'RESTRICTABLES': usage = RESTRICTABLE
    else: errors.append('Neither RETURNABLES or RESTRICTABLES assignment found')
    # join continuation lines back into one expression
    value = ''.join(line.strip().rstrip('\\').strip() for line in value.splitlines())
    try: value=ast.literal_eval(value)
    except Exception:
        errors.append('Second check (evalution) did not pass. Please check that your input is correct Python code.')
        raise ValidationError(errors)

    if not isinstance(value,dict):
        errors.append('The right-hand side is not a dictionary.')
        raise ValidationError(errors)

    for kw in value.keys():
        err = check_keyword_exists(kw)
        if err:
            errors.append(err)
            continue
        err = check_keyword_usage(kw,usage)
        if err: errors.append(err)
        if usage==RETURNABLE:
            err = check_returnvalues(kw,value[kw])
            if err: errors.append(err)
            err = check_unit(kw,value.keys())
            if err: errors.append(err)
    if errors: raise ValidationError(errors)

class CheckForm(forms.Form):
    content=forms.CharField(label='Paste your dictionary',
    widget=forms.widgets.Textarea(attrs={'cols':'80','rows':'25'}),
    required=True,validators=[validate_dict])

def check(request):
    if request.method == 'POST':
        form = CheckForm(request.POST)
        if form.is_valid():
            #print form.cleaned_data
            pass

    else:
        form=CheckForm()
    return render(request, 'browse/check.html', {'form': form})


#########
blockmap = {'so':'Source.',
'as':'AtomState.',
'ms':'MoleculeState.',
'mq':'MoleQNs.',
'ct':'CollTran.',
'rt':'RadTran.',
'me':'Method.',
'mo':'Molecule.',
'at':'AtomState.',
}

def makedicts(selected):
    content = 'RETURNABLES = {\\ \n'
    for kw in selected:
        if kw.usage.filter(name=RETURNABLE).exists():
            prefix = blockmap.get(kw.block,'')
            content += '\'%s\':\'%s\',\n'%(kw.name,prefix)

    content += '}\n\n\n'
    content += 'RESTRICTABLES = {\\ \n'
    for kw in selected:
        if kw.usage.filter(name=RESTRICTABLE).exists():
            content += '\'%s\':\'\',\n'%kw.name

    content += '}\n\n\n'
    return content

class SelectKeyWordFormSet(forms.models.BaseModelFormSet):
    def add_fields(self, form, index):
        super(SelectKeyWordFormSet, self).add_fields(form, index)
        form.fields["include"] = forms.BooleanField(required=False, label="Include this keyword")


def makenew(request):
    q = Q(usage__name=RESTRICTABLE) | Q(usage__name=RETURNABLE)
    queryset = KeyWord.objects.filter(q).distinct()
    # no editable model fields: the form only collects the "include" ticks,
    # everything shown comes from form.instance
    MakeNewFormSet = modelformset_factory(KeyWord,formset=SelectKeyWordFormSet,
                                          fields=(),extra=0)

    if request.method == 'POST':
        formset = MakeNewFormSet(request.POST,request.FILES,queryset=queryset)
        if formset.is_valid():
            selected=[]
            for form in formset.cleaned_data:
                if form['include']: selected.append(form['id'])

            filecontent = makedicts(selected)
            response=HttpResponse(filecontent,content_type='text/x-python')
            response['Content-Disposition'] = 'attachment; filename=dictionaries.py'
            return response

    else:
        formset = MakeNewFormSet(queryset=queryset)

    return render(request, 'browse/makenew.html', {'formset': formset})
