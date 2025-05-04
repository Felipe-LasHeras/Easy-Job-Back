# jobs/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    """Modelo extendido de usuario"""
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    es_prestador = models.BooleanField(default=False)

class Profesion(models.Model):
    """Profesiones para prestadores de servicios"""
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Profesión"
        verbose_name_plural = "Profesiones"

class Servicio(models.Model):
    """Servicios ofrecidos por prestadores"""
    prestador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='servicios')
    profesion = models.ForeignKey(Profesion, on_delete=models.PROTECT)
    tipo_servicio = models.CharField(max_length=100)
    descripcion = models.TextField()
    tarifa = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.tipo_servicio} - {self.prestador.username}"

class Trabajo(models.Model):
    """Trabajos contratados por clientes"""
    ESTADO_CHOICES = [
        ('agendado', 'Agendado'),
        ('en_proceso', 'En Proceso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]
    
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='trabajos_solicitados')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_trabajo = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='agendado')
    
    def __str__(self):
        return f"{self.servicio.tipo_servicio} - {self.cliente.username} - {self.estado}"

class Valoracion(models.Model):
    """Valoraciones de trabajos realizados"""
    trabajo = models.OneToOneField(Trabajo, on_delete=models.CASCADE)
    puntuacion = models.PositiveSmallIntegerField()  # 1 a 5 estrellas
    comentario = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Valoración de {self.trabajo.cliente.username} para {self.trabajo.servicio.prestador.username}"
    
    class Meta:
        verbose_name = "Valoración"
        verbose_name_plural = "Valoraciones"