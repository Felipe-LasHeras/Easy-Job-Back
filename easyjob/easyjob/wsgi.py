import os
import oracledb


oracledb.init_oracle_client(lib_dir=r"Z:\Documentos\Trabajos\instantclient-basic-windows.x64-23.8.0.25.04\instantclient_23_8")


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'easyjob.settings')


from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
