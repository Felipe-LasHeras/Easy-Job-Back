import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'easyjob.settings')


import os
import oracledb
from django.core.wsgi import get_wsgi_application


oracledb.init_oracle_client(lib_dir=r"Z:\Documentos\Trabajos\instantclient-basic-windows.x64-23.8.0.25.04\instantclient_23_8")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'easyjob.settings')


application = get_wsgi_application()