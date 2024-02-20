from django import template
from menu.models import MenuItem
from django.template import Context
import re

register = template.Library()


@register.inclusion_tag('menu/draw_menu_tag.html', takes_context=True)
def draw_menu(context: Context, menu_name: str):
    url_path = context.request.path
    menu_item = MenuItem.objects.filter(menu__name=menu_name).order_by('path')

    target_path, target_lvl = None, None
    for item in menu_item:
        if item.url == url_path:
            target_path, target_lvl = item.path, item.level
            break

    menu_items_list = []
    for item in menu_item:

        if target_path is None or target_lvl is None:
            if item.level == 0:
                menu_items_list.append(item)
            continue

        # Добавляем корневые элементы
        if item.level == 0:
            menu_items_list.append(item)
            continue

        # Добавляем ближайших потомков
        pattern = target_path + r'.\d{1}$'
        if re.match(pattern, item.path):
            menu_items_list.append(item)
            continue

        # Добавляем всех родителей и их соседей
        for i in range(target_lvl):
            pattern = target_path[:(i*2+1)] + r'.\d{1}$'
            if re.match(pattern, item.path):
                menu_items_list.append(item)
                break

    return {'items': menu_items_list, 'urlpath': url_path}
