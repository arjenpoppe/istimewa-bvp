"""
WSGI config for bvp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os, sys

sys.path.append('C:\\Users\\Administrator\\Bitnami Django Stack projects\\bvp')

os.environ.setdefault("PYTHON_EGG_CACHE", "C:\\Users\\Administrator\\Bitnami Django Stack projects\\bvp\\egg_cache")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bvp.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
