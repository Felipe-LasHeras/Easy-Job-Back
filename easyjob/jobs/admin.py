# jobs/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Profesion, Servicio, Trabajo, Valoracion

class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'es_prestador', 'is_staff')
    list_filter = ('es_prestador', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('telefono', 'direccion', 'fecha_nacimiento', 'es_prestador')}),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')

class ServicioAdmin(admin.ModelAdmin):
    list_display = ('tipo_servicio', 'prestador', 'profesion', 'tarifa', 'activo')
    list_filter = ('activo', 'profesion')
    search_fields = ('tipo_servicio', 'descripcion', 'prestador__username')

class TrabajoAdmin(admin.ModelAdmin):
    list_display = ('servicio', 'cliente', 'fecha_solicitud', 'estado')
    list_filter = ('estado', 'fecha_solicitud')
    search_fields = ('servicio__tipo_servicio', 'cliente__username')

class ValoracionAdmin(admin.ModelAdmin):
    list_display = ('trabajo', 'puntuacion', 'fecha')
    list_filter = ('puntuacion', 'fecha')

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Profesion)
admin.site.register(Servicio, ServicioAdmin)
admin.site.register(Trabajo, TrabajoAdmin)
admin.site.register(Valoracion, ValoracionAdmin)