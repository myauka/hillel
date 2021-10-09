from django.core.management import execute_from_command_line
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import path
from django.conf import settings
import importlib.util


settings.configure(
    DEBUG=True,  # делает джанго терпимым к некоторым пропущенным вещам
    ROOT_URLCONF=__name__,  # говорит джанго искать конфигурацию в этом же модуле
    SECRET_KEY='ASDA',
)


TEMPLATE = """
<!DOCTYPE html>
<html>
 <head>
  <title>Homework1</title>
 </head>
 <body>
 {content}
 </body>
</html>
"""


def import_module(mod_name):
    module = importlib.util.module_from_spec(mod_name)
    mod_name.loader.exec_module(module)
    return module


def check_module(mod_name):
    module_spec = importlib.util.find_spec(mod_name)
    if module_spec is None:
        return None  # если модуля нет то нон
    else:
        return module_spec


def handler(request):
    return HttpResponse(TEMPLATE.format(content='не забывайте /doc/ !'))


def mod_handler(request, mod_name):
    module_spec = check_module(mod_name=mod_name)
    if not module_spec:
        return HttpResponseNotFound()
    module = import_module(mod_name=module_spec)
    links = [f'<a href="{mod_name}/{obj}">{obj}</a><br>' for obj in dir(module) if not obj.startswith('__')]
    return HttpResponse(TEMPLATE.format(content=''.join(links),
                                        content_type='text/plain'))


def obj_handler(request, mod_name, obj_name):
    module_spec = check_module(mod_name=mod_name)
    if not module_spec:
        return HttpResponseNotFound()
    module = import_module(mod_name=module_spec)

    if obj_name not in dir(module):
        return HttpResponseNotFound()

    return HttpResponse(TEMPLATE.format(content=getattr(__import__(mod_name), obj_name).__doc__))


urlpatterns = [  # роутер
    path('', handler),  # функция обработчик. В данном кейсе вызывается при попытке доступа к корню (/) страницы
    path('doc/<mod_name>', mod_handler),
    path('doc/<mod_name>/<obj_name>', obj_handler),
]


if __name__ == '__main__':
    execute_from_command_line()
