# jobs/api_urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import api_views

router = DefaultRouter()
router.register(r'servicios', api_views.ServicioViewSet, basename='servicio')
router.register(r'trabajos', api_views.TrabajoViewSet, basename='trabajo')
router.register(r'valoraciones', api_views.ValoracionViewSet, basename='valoracion')
router.register(r'publicaciones-empleo', api_views.PublicacionEmpleoViewSet, basename='publicacion_empleo')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('status/', api_views.APIStatusView.as_view(), name='api_status'),
    path('mis-servicios/', api_views.mis_servicios, name='mis_servicios'),
]