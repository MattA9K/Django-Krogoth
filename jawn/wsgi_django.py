# entry point for the Django loop
from django.core.wsgi import get_wsgi_application
import uwsgi
from uwsgidecorators import timer
from django.utils import autoreload
# from django.utils.autoreload import autoreload_started
import os
import os.path

@timer(1)
def change_code_gracefull_reload(sig):
    if os.path.isfile('/usr/src/app/RELOAD.TXT'):
        os.remove('/usr/src/app/RELOAD.TXT')
        uwsgi.reload()

#     if autoreload.file_changed():
#         if autoreload.code_changed():
#             uwsgi.reload()

# def my_watchdog(sender, **kwargs):
#     sender.watch_dir('/usr/src/app')


application = get_wsgi_application()
autoreload_started.connect(my_watchdog)