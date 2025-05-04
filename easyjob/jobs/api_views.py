# jobs/api_views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Servicio, Trabajo, Valoracion, Profesion
from .serializers import ServicioSerializer, TrabajoSerializer, ValoracionSerializer, ProfesionSerializer

class ServicioViewSet(viewsets.ModelViewSet):
    """API para gestionar servicios"""
    queryset = Servicio.objects.filter(activo=True)
    serializer_class = ServicioSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filtrar servicios según el tipo de usuario"""
        user = self.request.user
        if user.es_prestador:
            # Los prestadores solo pueden ver sus propios servicios
            return Servicio.objects.filter(prestador=user)
        else:
            # Los clientes pueden ver todos los servicios activos
            return Servicio.objects.filter(activo=True)

class TrabajoViewSet(viewsets.ReadOnlyModelViewSet):
    """API para consultar trabajos"""
    queryset = Trabajo.objects.all()
    serializer_class = TrabajoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filtrar trabajos según el tipo de usuario"""
        user = self.request.user
        if user.es_prestador:
            # Los prestadores ven trabajos en sus servicios
            return Trabajo.objects.filter(servicio__prestador=user)
        else:
            # Los clientes ven sus propios trabajos
            return Trabajo.objects.filter(cliente=user)

class ValoracionViewSet(viewsets.ReadOnlyModelViewSet):
    """API para consultar valoraciones"""
    queryset = Valoracion.objects.all()
    serializer_class = ValoracionSerializer
    permission_classes = [permissions.IsAuthenticated]

class APIStatusView(APIView):
    """Vista para verificar el estado de la API"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        return Response({
            'status': 'ok',
            'message': 'API de Easy Job funcionando correctamente',
            'version': '1.0'
        })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def mis_servicios(request):
    """API para que los prestadores vean sus servicios"""
    if request.user.es_prestador:
        servicios = Servicio.objects.filter(prestador=request.user)
        serializer = ServicioSerializer(servicios, many=True)
        return Response(serializer.data)
    else:
        return Response({'error': 'Usuario no es prestador'}, status=status.HTTP_403_FORBIDDEN)