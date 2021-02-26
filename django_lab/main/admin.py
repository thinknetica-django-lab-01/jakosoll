from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import gettext_lazy as _
from ckeditor.widgets import CKEditorWidget
from django import forms
from .models import Product


class FlatAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())


class FlatPageAdmin(FlatPageAdmin):
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites')}),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': (
                'enable_comments',
                'registration_required',
                'template_name',
            ),
        }),
    )
    form = FlatAdminForm


def archive_event(modeladmin, request, queryset):
    for obj in queryset:
        if obj.available:
            obj.available = False
        obj.save()


archive_event.short_description = 'Добавить записи в архив'


def public_event(modeladmin, request, queryset):
    for obj in queryset:
        if not obj.available:
            obj.available = True
        obj.save()


public_event.short_description = 'Опубликовать записи'


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price',)
    list_display_links = ('name', 'category',)
    list_filter = ('category', 'tags', 'created', 'available')
    list_editable = ('price',)
    search_fields = ('name',)
    actions = [archive_event, public_event]


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
admin.site.register(Product, ProductAdmin)
