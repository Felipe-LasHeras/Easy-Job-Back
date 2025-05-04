# Easy Job - Plataforma de Servicios Profesionales

## Descripción

Easy Job es una plataforma web que conecta prestadores de servicios profesionales con clientes que necesitan estos servicios. Este proyecto implementa un sistema completo con Django, Django REST Framework y consume APIs externas.

## Características principales

- Registro de usuarios (clientes y prestadores)
- Autenticación y protección de rutas
- Gestión de perfiles
- Publicación y búsqueda de servicios
- Contratación de servicios
- Valoraciones y comentarios
- API REST con autenticación JWT
- Consumo de APIs externas (Clima, Monedas, etc.)

## APIs REST Propias

La aplicación cuenta con dos APIs REST principales:

1. **API de Servicios** (`/api/servicios/`)
   - GET: Listar servicios
   - POST: Crear servicios (solo prestadores)
   - GET/{id}: Obtener servicio específico
   - PUT/{id}: Actualizar servicio
   - DELETE/{id}: Eliminar servicio

2. **API de Trabajos** (`/api/trabajos/`)
   - GET: Listar trabajos (filtrado según usuario)