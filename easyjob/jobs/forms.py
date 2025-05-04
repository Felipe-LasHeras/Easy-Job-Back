# jobs/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from .models import Usuario, Servicio

class RegistroUsuarioForm(UserCreationForm):
    """Formulario de registro de usuario"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True, label="Nombre")
    last_name = forms.CharField(required=True, label="Apellido")
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
        label="Fecha de nacimiento"
    )
    es_prestador = forms.BooleanField(
        required=False,
        label="Soy prestador de servicios",
        initial=False
    )
    terminos = forms.BooleanField(
        required=True,
        label="Acepto los términos y condiciones"
    )
    
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'first_name', 'last_name', 'fecha_nacimiento', 
                  'es_prestador', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está en uso.")
        return email

class EditarPerfilForm(forms.ModelForm):
    """Formulario para editar el perfil"""
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'telefono', 'direccion']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico',
            'telefono': 'Teléfono',
            'direccion': 'Dirección'
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

class CambiarPasswordForm(forms.Form):
    """Formulario para cambiar contraseña"""
    password_actual = forms.CharField(
        widget=forms.PasswordInput(),
        label="Contraseña actual",
        required=True
    )
    password_nueva = forms.CharField(
        widget=forms.PasswordInput(),
        label="Nueva contraseña",
        required=True,
        min_length=6
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(),
        label="Confirmar nueva contraseña",
        required=True
    )
    
    def clean(self):
        cleaned_data = super().clean()
        password_nueva = cleaned_data.get('password_nueva')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password_nueva and password_confirm and password_nueva != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden")
            
        return cleaned_data

class RecuperacionPasswordForm(forms.Form):
    """Formulario para recuperar contraseña"""
    email = forms.EmailField(
        required=True,
        label="Correo electrónico"
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("No existe una cuenta con este correo electrónico.")
        return email

class CodigoVerificacionForm(forms.Form):
    """Formulario para ingresar código de verificación"""
    codigo = forms.CharField(
        max_length=6,
        required=True,
        label="Código de verificación"
    )

class ServicioForm(forms.ModelForm):
    """Formulario para crear/editar servicios"""
    class Meta:
        model = Servicio
        fields = ['profesion', 'tipo_servicio', 'descripcion', 'tarifa']
        labels = {
            'profesion': 'Profesión',
            'tipo_servicio': 'Tipo de servicio',
            'descripcion': 'Descripción',
            'tarifa': 'Tarifa por hora (CLP)'
        }
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }