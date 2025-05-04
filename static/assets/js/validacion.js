// Validaciones generales para los formularios de Easy Job

document.addEventListener('DOMContentLoaded', function() {
  // Validación para el formulario de registro
  const registroForm = document.getElementById('registroForm');
  if (registroForm) {
      registroForm.addEventListener('submit', validarRegistro);
  }
  
  // Validación para el formulario de login
  const loginForm = document.getElementById('loginForm');
  if (loginForm) {
      loginForm.addEventListener('submit', validarLogin);
  }
  
  // Validación para el formulario de recuperación de contraseña
  const recuperacionForm = document.getElementById('recuperacionForm');
  if (recuperacionForm) {
      recuperacionForm.addEventListener('submit', validarRecuperacion);
  }
});

// Función para validar el formulario de registro (simplificada)
function validarRegistro(event) {
  event.preventDefault();
  
  let isValid = true;
  
  // Validar campos básicos
  const campos = ['nombreCompleto', 'usuario', 'email', 'password', 'confirmPassword'];
  
  campos.forEach(function(campo) {
    const elemento = document.getElementById(campo);
    if (elemento && elemento.value.trim() === '') {
      setInvalid(elemento, 'Este campo es obligatorio');
      isValid = false;
    } else if (elemento) {
      setValid(elemento);
    }
  });
  
  // Validar email
  const email = document.getElementById('email');
  if (email && email.value.trim() !== '') {
    if (!email.value.includes('@')) {
      setInvalid(email, 'Por favor ingresa un correo electrónico válido');
      isValid = false;
    }
  }
  
  // Validar coincidencia de contraseñas
  const password = document.getElementById('password');
  const confirmPassword = document.getElementById('confirmPassword');
  if (password && confirmPassword && password.value !== '' && confirmPassword.value !== '') {
    if (password.value !== confirmPassword.value) {
      setInvalid(confirmPassword, 'Las contraseñas no coinciden');
      isValid = false;
    }
  }
  
  // Validar términos y condiciones
  const terminos = document.getElementById('terminos');
  if (terminos && !terminos.checked) {
    setInvalid(terminos, 'Debes aceptar los términos y condiciones');
    isValid = false;
  }
  
  if (isValid) {
    alert('Registro exitoso! Ahora puedes iniciar sesión.');
    window.location.href = 'login.html';
  }
}

// Función para validar el formulario de login (simplificada)
function validarLogin(event) {
  event.preventDefault();
  
  let isValid = true;
  
  // Validar username
  const username = document.getElementById('username');
  if (username && username.value.trim() === '') {
    setInvalid(username, 'Por favor ingresa tu nombre de usuario');
    isValid = false;
  } else if (username) {
    setValid(username);
  }
  
  // Validar password
  const password = document.getElementById('password');
  if (password && password.value.trim() === '') {
    setInvalid(password, 'Por favor ingresa tu contraseña');
    isValid = false;
  } else if (password) {
    setValid(password);
  }
  
  if (isValid) {
    // Simulación de login exitoso
    if (username.value === 'cliente') {
      window.location.href = 'perfiles-clientes.html';
    } else if (username.value === 'prestador') {
      window.location.href = 'editor-perfil.html';
    } else {
      alert('Usuario o contraseña incorrectos');
    }
  }
}

// Función para validar el formulario de recuperación de contraseña (simplificada)
function validarRecuperacion(event) {
  event.preventDefault();
  
  const email = document.getElementById('email');
  if (!email.value.includes('@')) {
    setInvalid(email, 'Por favor ingresa un correo electrónico válido');
  } else {
    setValid(email);
    // Pasar al siguiente paso
    document.getElementById('paso1').style.display = 'none';
    document.getElementById('paso2').style.display = 'block';
  }
}

// Funciones auxiliares para manejo de validaciones (simplificadas)
function setInvalid(element, message) {
  element.classList.add('is-invalid');
  element.classList.remove('is-valid');
  
  // Si hay un elemento de feedback, actualizarlo con el mensaje
  const feedback = element.nextElementSibling;
  if (feedback && feedback.classList.contains('invalid-feedback')) {
    feedback.textContent = message;
  }
}

function setValid(element) {
  element.classList.remove('is-invalid');
  element.classList.add('is-valid');
}