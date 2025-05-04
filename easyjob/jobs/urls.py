# jobs/urls.py
from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    # Páginas públicas
    path('', views.home, name='home'),
    path('registro/', views.registro_view, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('recuperacion-password/', views.recuperacion_password_view, name='recuperacion_password'),
    path('verificacion-codigo/', views.verificacion_codigo_view, name='verificacion_codigo'),
    
    # Páginas protegidas (requieren login)
    path('editar-perfil/', views.editar_perfil_view, name='editar_perfil'),
    path('perfil-cliente/', views.perfil_cliente_view, name='perfil_cliente'),
    path('mis-trabajos/', views.mis_trabajos_view, name='mis_trabajos'),
    
    # Servicios
    path('servicios/', views.servicios_view, name='servicios'),
    path('servicios/<int:servicio_id>/', views.detalle_servicio_view, name='detalle_servicio'),
    path('servicios/<int:servicio_id>/contratar/', views.contratar_servicio_view, name='contratar_servicio'),
]