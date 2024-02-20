from django.contrib import admin
from . import models


class MenuItemInline(admin.TabularInline):
    model = models.MenuItem
    can_delete = False
    extra = 0
    fields = ('name', 'parent', 'url')

    def get_formset(self, request, obj=None, **kwargs):
        """
        Убираем из выбора родительского элемента MenuItems,
        которые не относятся к текущему меню
        """
        formset = super().get_formset(request, obj=obj, **kwargs)
        formset.form.base_fields['parent'].queryset = models.MenuItem.objects.filter(menu__name=obj.name)
        return formset


class MenuAdmin(admin.ModelAdmin):
    model = models.Menu
    inlines = [MenuItemInline]

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            # hide MyInline in the add view
            if not isinstance(inline, MenuItemInline) or obj is not None:
                yield inline.get_formset(request, obj), inline


admin.site.register(models.Menu, MenuAdmin)
