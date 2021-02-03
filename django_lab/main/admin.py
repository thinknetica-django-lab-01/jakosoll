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


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    list_display_links = ('name', 'category',)
    list_filter = ('category',)
    list_editable = ('price',)
    search_fields = ('name',)


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
admin.site.register(Product, ProductAdmin)
