"""
WSGI config for bvp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
# site.addsitedir('C:/users/administrator/envs/bvp/lib/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('c:/users/administrator/documents/istimewa-bvp')
sys.path.append('c:/users/administrator/documents/istimewa-bvp/bvp')

os.environ['DJANGO_SETTINGS_MODULE'] = 'bvp.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bvp.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
