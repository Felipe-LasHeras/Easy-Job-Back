# jobs/serializers.py
from rest_framework import serializers
from .models import Usuario, Servicio, Trabajo, Profesion, Valoracion

class ProfesionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesion
        fields = '__all__'

class UsuarioPublicoSerializer(serializers.ModelSerializer):
    """Serializador con información pública del usuario"""
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'es_prestador']

class ServicioSerializer(serializers.ModelSerializer):
    profesion = ProfesionSerializer(read_only=True)
    prestador = UsuarioPublicoSerializer(read_only=True)
    
    class Meta:
        model = Servicio
        fields = [
            'id', 'tipo_servicio', 'descripcion', 'tarifa', 
            'activo', 'fecha_creacion', 'profesion', 'prestador'
        ]
        read_only_fields = ['prestador']
    
    def create(self, validated_data):
        # Obtener el usuario actual de la solicitud
        request = self.context.get('request')
        validated_data['prestador'] = request.user
        return super().create(validated_data)

class TrabajoSerializer(serializers.ModelSerializer):
    servicio = ServicioSerializer(read_only=True)
    cliente = UsuarioPublicoSerializer(read_only=True)
    
    class Meta:
        model = Trabajo
        fields = [
            'id', 'fecha_solicitud', 'fecha_trabajo', 'estado', 
            'servicio', 'cliente'
        ]

class ValoracionSerializer(serializers.ModelSerializer):
    trabajo = TrabajoSerializer(read_only=True)
    
    class Meta:
        model = Valoracion
        fields = ['id', 'puntuacion', 'comentario', 'fecha', 'trabajo']