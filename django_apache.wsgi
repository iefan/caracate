import os
import sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'caracate.settings'
sys.path.append('D:/caracate')
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()