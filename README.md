## Древовидное меню

В приложении menu реализована возможность создания, редактирования и отображения древовидного меню.
Для отображения в другом django-app необходимо загрузить тэги меню <code>{% load menu_tags %}</code> и вызвать тэг, передав туда Menu.name.
<code>{% draw_menu 'menu.name' %}</code>

Реализация предполагает, что у каждого пункта меню есть свой собственный, уникальный url.
Хранение дерева реализована с помощью Materialized Path, что даёт возможость хранить его в любой sql - базе данных.

### Быстрый старт

<pre>pip install -r requirements.txt</pre>
<pre>export SECRET_KEY='some_key'</pre>

<pre>python manage.py migrate</pre>

Для быстрой демонстрации возможностей в приложении добавлен готовый набор fixtures, содержащий готовые меню. Загрузите их с помощью:
<pre>python manage.py loaddata fixtures/menu.json --app app.menu</pre>

Если проект запускается на боевом сервере - установите: <code>DEBUG = False</code>

Приложение с именем app добавлен, как пример стороннее django-app для демонстрации применения menu.
Запустите
<pre>python manage.py runserver</pre>

и перейдите по адресу http://127.0.0.1:8000/


### Редактирование/ создание меню

Редактирование и создание меню осуществляется в стандартном админ-интерфейсе Django. Для каждого интстанса меню можно настроить его элементы, указав Имя, Url-путь и родителя.
