"""
WSGI config for cdj_proj project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

from django.core.wsgi import get_wsgi_application
from dj_static import Cling

import os

import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cdj_proj.settings")

from django.core.wsgi import get_wsgi_application


if settings.DEBUG:
    application = get_wsgi_application()
else:
    application = Cling(get_wsgi_application())
