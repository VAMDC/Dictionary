from django.contrib import admin
from .models import KeyWord, Usage

RETURNABLE = 'Returnable'
REQUESTABLE = 'Requestable'
RESTRICTABLE = 'Restrictable'

def usage(name):
    """Looked up per call: the database must not be touched at import time."""
    return Usage.objects.get(name=name)

def keywords(obj):
    return ', '.join([o.name for o in obj.keyword_set.iterator()])

def make_returnable(modeladmin, request, queryset):
    for kw in queryset: kw.usage.add(usage(RETURNABLE))
#    LogEntry.objects.log_action( user=request.user,
#				change_message='')
make_returnable.short_description = "Mark selected keywords Returnable"

def unmake_returnable(modeladmin, request, queryset):
    for kw in queryset: kw.usage.remove(usage(RETURNABLE))
unmake_returnable.short_description = "Unmark selected keywords Returnable"

def make_requestable(modeladmin, request, queryset):
    for kw in queryset: kw.usage.add(usage(REQUESTABLE))
make_requestable.short_description = "Mark selected keywords Requestable"

def unmake_requestable(modeladmin, request, queryset):
    for kw in queryset: kw.usage.remove(usage(REQUESTABLE))
unmake_requestable.short_description = "Unmark selected keywords Requestable"

def make_restrictable(modeladmin, request, queryset):
    for kw in queryset: kw.usage.add(usage(RESTRICTABLE))
make_restrictable.short_description = "Mark selected keywords Restrictable"

def unmake_restrictable(modeladmin, request, queryset):
    for kw in queryset: kw.usage.remove(usage(RESTRICTABLE))
unmake_restrictable.short_description = "Unmark selected keywords Restrictable"

def toggle_datatype(modeladmin, request, queryset):
    for kw in queryset:
        kw.datatype = not kw.datatype
        kw.save()
toggle_datatype.short_description = "Toggle DataType true/false for selected keywords"

class KeyWordAdmin(admin.ModelAdmin):
    list_display = ('name', 'sdescr','datatype','unit','list_usages')
    search_fields = ('name', 'sdescr', 'ldescr', 'unit')
    actions_on_top = True
    actions_on_bottom = True
    actions = [toggle_datatype,make_returnable,unmake_returnable,unmake_requestable,make_requestable, make_restrictable, unmake_restrictable]

class UsageAdmin(admin.ModelAdmin):
    list_display = ('name',keywords)

admin.site.register(KeyWord,KeyWordAdmin)
admin.site.register(Usage,UsageAdmin)

