from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Menu(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название меню')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'menu'
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, related_name='items', on_delete=models.CASCADE)
    url = models.CharField(max_length=32, verbose_name='Путь', unique=True)
    name = models.CharField(max_length=32, verbose_name='Наименование')
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
                               null=True, blank=True, verbose_name='Родительский элемент')
    path = models.CharField(max_length=32, blank=True)
    level = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return '%s (id: %s)' % (self.name, self.id)

    class Meta:
        db_table = 'menu_item'
        verbose_name = 'Элемент меню'
        verbose_name_plural = 'Элементы меню'


@receiver(signal=pre_save, sender=MenuItem)
def before_save_menu_item(instance, **kwargs):
    if instance.url.startswith('/') is False:
        instance.url = '/' + instance.url

    if not instance.parent:
        count = MenuItem.objects.filter(level=1, menu=instance.menu)
        instance.path = str(count.count() + 1)
        instance.level = 0
    else:
        path = instance.parent.path + '.'
        lvl = instance.parent.level + 1
        count = MenuItem.objects.filter(path__contains=path, level=lvl, menu=instance.menu)
        instance.path = '%s.%s' % (instance.parent.path, count.count() + 1)
        instance.level = instance.parent.level + 1
