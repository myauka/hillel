import random
import secrets
import string
from django.core.management import execute_from_command_line
from django.urls import path
from django.conf import settings
from django.db import connection
from django.shortcuts import redirect, render


settings.configure(
    DEBUG=True,
    ROOT_URLCONF=__name__,
    SECRET_KEY='ASDA',
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [''],
        }
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'short_links.sqlite3'
        }
    }
)


def create_database():
    create_query = '''
    create table if not exists short_links (
    id CHAR(100),
    link CHAR(100)
    );
    '''
    with connection.cursor() as cur:
        cur.execute(create_query)


def generate_link_id():
    alphabet = string.ascii_letters + string.digits
    size = random.randint(5, 6)
    link_id = ''.join(secrets.choice(alphabet) for _ in range(size))
    return link_id


def insert_link(link):
    insert_link_query = ''' 
    insert into short_links values(%s, %s);
    '''
    link_id = generate_link_id()
    with connection.cursor() as cur:
        cur.executemany(insert_link_query, [(link_id, link)])
    return link_id


def get_link_by_id(link_id):
    select_link_query = f'''
    select link from short_links where id=%s;
    '''
    with connection.cursor() as cur:
        cur.execute(select_link_query, [link_id])
        res = cur.fetchone()
    return res[0]


def redirect_by_id(request, link_id):
    link = get_link_by_id(link_id)
    return redirect(link)


def main_page_handler(request):
    content = {
        'response': '',
        'link_by_id': '',
        }
    if request.method == 'POST':
        if request.POST['url'].startswith(('http',
                                               'https', 'ftp')):
            link_id = insert_link(request.POST['url'])
            content['link_by_id'] = link_id
        else:
            content['response'] = 'Wrong protocol! We only support http, https, ftp'
    return render(request, 'index.html', content)


urlpatterns = [
    path('', main_page_handler),
    path('<link_id>', redirect_by_id)
]

if __name__ == '__main__':
    create_database()
    execute_from_command_line()
