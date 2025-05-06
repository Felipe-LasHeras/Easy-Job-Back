# jobs/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from .models import Usuario, Servicio, Trabajo, Profesion
from .forms import (RegistroUsuarioForm, EditarPerfilForm, CambiarPasswordForm, 
                    RecuperacionPasswordForm, CodigoVerificacionForm, ServicioForm)
from .external_apis import ExternalAPIManager 
from django.conf import settings

def home(request):
    """Vista para la página principal"""
    return render(request, 'jobs/index.html')

def registro_view(request):
    """Vista para registro de usuarios"""
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, '¡Registro exitoso! Ahora puedes usar Easy Job.')
            if usuario.es_prestador:
                return redirect('editar_perfil')
            else:
                return redirect('home')
    else:
        form = RegistroUsuarioForm()
    
    return render(request, 'jobs/registro.html', {'form': form})

def login_view(request):
    """Vista para inicio de sesión"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido de nuevo, {user.first_name}!')
            if user.es_prestador:
                return redirect('mis_trabajos')
            else:
                return redirect('perfil_cliente')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
            
    return render(request, 'jobs/login.html')

def recuperacion_password_view(request):
    """Vista para recuperación de contraseña (paso 1)"""
    if request.method == 'POST':
        form = RecuperacionPasswordForm(request.POST)
        if form.is_valid():
            # En un entorno real, aquí enviarías un correo con un token
            # Para este ejercicio, simplemente mostramos la siguiente pantalla
            email = form.cleaned_data['email']
            request.session['recovery_email'] = email
            messages.success(request, 'Se ha enviado un código de verificación a tu correo electrónico.')
            return redirect('verificacion_codigo')
    else:
        form = RecuperacionPasswordForm()
    
    return render(request, 'jobs/recuperacion_password.html', {'form': form})

def verificacion_codigo_view(request):
    """Vista para verificación de código (paso 2)"""
    if 'recovery_email' not in request.session:
        messages.error(request, 'Debes solicitar un código de recuperación primero.')
        return redirect('recuperacion_password')
    
    if request.method == 'POST':
        form = CodigoVerificacionForm(request.POST)
        if form.is_valid():
            # En un entorno real, validaríamos el código
            # Para este ejercicio, cualquier código es válido
            messages.success(request, 'Código verificado correctamente. Ahora puedes crear una nueva contraseña.')
            return redirect('login')
    else:
        form = CodigoVerificacionForm()
    
    return render(request, 'jobs/verificacion_codigo.html', {'form': form})

@login_required
def editar_perfil_view(request):
    """Vista para editar perfil"""
    if request.method == 'POST':
        if 'guardar_perfil' in request.POST:
            form = EditarPerfilForm(request.POST, instance=request.user)
            password_form = CambiarPasswordForm()
            if form.is_valid():
                form.save()
                messages.success(request, 'Perfil actualizado correctamente')
                return redirect('editar_perfil')
        elif 'cambiar_password' in request.POST:
            form = EditarPerfilForm(instance=request.user)
            password_form = CambiarPasswordForm(request.POST)
            if password_form.is_valid():
                user = request.user
                if user.check_password(password_form.cleaned_data['password_actual']):
                    user.set_password(password_form.cleaned_data['password_nueva'])
                    user.save()
                    update_session_auth_hash(request, user)  # Mantener la sesión activa
                    messages.success(request, 'Contraseña actualizada correctamente')
                else:
                    messages.error(request, 'La contraseña actual es incorrecta')
                return redirect('editar_perfil')
    else:
        form = EditarPerfilForm(instance=request.user)
        password_form = CambiarPasswordForm()
    
    context = {
        'form': form,
        'password_form': password_form,
    }
    
    # Si es prestador, mostrar también el formulario de servicios
    if request.user.es_prestador:
        # Obtener profesiones y servicios
        profesiones = Profesion.objects.all()
        servicios = Servicio.objects.filter(prestador=request.user)
        
        # Procesar formulario de servicio
        if request.method == 'POST' and 'guardar_servicio' in request.POST:
            servicio_form = ServicioForm(request.POST)
            if servicio_form.is_valid():
                servicio = servicio_form.save(commit=False)
                servicio.prestador = request.user
                servicio.save()
                messages.success(request, 'Servicio guardado correctamente')
                return redirect('editar_perfil')
        else:
            servicio_form = ServicioForm()
        
        context.update({
            'profesiones': profesiones,
            'servicios': servicios,
            'servicio_form': servicio_form
        })
    
    return render(request, 'jobs/editar_perfil.html', context)

@login_required
def perfil_cliente_view(request):
    """Vista para el perfil de cliente"""
    if not request.user.es_prestador:
        trabajos = Trabajo.objects.filter(cliente=request.user).order_by('-fecha_solicitud')
        return render(request, 'jobs/perfil_cliente.html', {'trabajos': trabajos})
    else:
        messages.warning(request, 'Esta sección es solo para clientes')
        return redirect('mis_trabajos')

@login_required
def mis_trabajos_view(request):
    """Vista para los trabajos del prestador"""
    if request.user.es_prestador:
        servicios = Servicio.objects.filter(prestador=request.user)
        trabajos = Trabajo.objects.filter(servicio__in=servicios).order_by('-fecha_solicitud')
        valoraciones = []
        for servicio in servicios:
            trabajos_completados = Trabajo.objects.filter(servicio=servicio, estado='completado')
            valoraciones_servicio = Valoracion.objects.filter(trabajo__in=trabajos_completados)
            if valoraciones_servicio.exists():
                valoraciones.extend(valoraciones_servicio)
        return render(request, 'jobs/mis_trabajos.html', {'trabajos': trabajos, 'valoraciones': valoraciones})
    else:
        messages.warning(request, 'Esta sección es solo para prestadores de servicios')
        return redirect('perfil_cliente')

def servicios_view(request):
    """Vista para listar servicios disponibles"""
    servicios_list = Servicio.objects.filter(activo=True).order_by('-fecha_creacion')
    # Filtrado opcional
    profesion_id = request.GET.get('profesion')
    if profesion_id:
        servicios_list = servicios_list.filter(profesion_id=profesion_id)
    
    profesiones = Profesion.objects.all()
    return render(request, 'jobs/servicios.html', {
        'servicios': servicios_list,
        'profesiones': profesiones,
        'profesion_seleccionada': profesion_id
    })

@login_required
def detalle_servicio_view(request, servicio_id):
    """Vista para ver detalle de un servicio"""
    servicio = get_object_or_404(Servicio, pk=servicio_id, activo=True)
    # Obtener valoraciones del prestador
    trabajos_prestador = Trabajo.objects.filter(
        servicio__prestador=servicio.prestador,
        estado='completado'
    )
    valoraciones = Valoracion.objects.filter(trabajo__in=trabajos_prestador)
    
    return render(request, 'jobs/detalle_servicio.html', {
        'servicio': servicio,
        'valoraciones': valoraciones
    })

@login_required
def contratar_servicio_view(request, servicio_id):
    """Vista para contratar un servicio"""
    servicio = get_object_or_404(Servicio, pk=servicio_id, activo=True)
    
    # No permitir que un prestador contrate su propio servicio
    if request.user == servicio.prestador:
        messages.error(request, 'No puedes contratar tu propio servicio')
        return redirect('servicios')
    
    if request.method == 'POST':
        # Crear un nuevo trabajo
        trabajo = Trabajo.objects.create(
            servicio=servicio,
            cliente=request.user,
            estado='agendado'
        )
        messages.success(request, f'Has contratado el servicio "{servicio.tipo_servicio}" exitosamente')
        return redirect('perfil_cliente')
    
    return render(request, 'jobs/contratar_servicio.html', {'servicio': servicio})


@login_required
def api_externa_view(request):
    """Vista para mostrar datos de APIs externas"""
    from .external_apis import ExternalAPIManager
    
    clima = ExternalAPIManager.get_weather_data()
    monedas = ExternalAPIManager.get_exchange_rates()
    noticias = ExternalAPIManager.get_news()
    usuarios = ExternalAPIManager.get_random_facts()
    
    context = {
        'clima': clima,
        'monedas': monedas,
        'noticias': noticias,
        'usuarios': usuarios
    }
    
    return render(request, 'jobs/api_externa.html', context)


external_data_view = api_externa_view

