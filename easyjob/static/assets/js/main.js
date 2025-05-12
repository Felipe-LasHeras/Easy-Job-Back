// Archivo JavaScript principal para Easy Job

document.addEventListener('DOMContentLoaded', function() {
  // Inicializar tooltips de Bootstrap (versión simplificada)
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl);
  });
  
  // Evento para la barra de búsqueda
  const searchForm = document.querySelector('.search-form');
  if (searchForm) {
      searchForm.addEventListener('submit', function(event) {
          event.preventDefault();
          const searchTerm = this.querySelector('input').value.trim();
          if (searchTerm !== '') {
              // Aquí iría la lógica de búsqueda
              console.log('Buscando:', searchTerm);
          }
      });
  }
  
  // Función para mostrar/ocultar el botón de volver arriba
  const btnScrollTop = document.getElementById('btn-scroll-top');
  if (btnScrollTop) {
      window.addEventListener('scroll', function() {
          if (window.pageYOffset > 300) {
              btnScrollTop.style.display = 'block';
          } else {
              btnScrollTop.style.display = 'none';
          }
      });
      
      btnScrollTop.addEventListener('click', function() {
          window.scrollTo({
              top: 0,
              behavior: 'smooth'
          });
      });
  }
});

// Función para mostrar mensajes de alerta
function showAlert(message, type = 'success') {
  alert(message);
}