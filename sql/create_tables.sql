-- Creación de tablas para la aplicación Easy Job
-- Nota: En producción, estas tablas serán creadas automáticamente por Django

-- Secuencias para las PK
CREATE SEQUENCE jobs_usuario_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE jobs_profesion_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE jobs_servicio_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE jobs_trabajo_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE jobs_valoracion_seq START WITH 1 INCREMENT BY 1;

-- Tabla de Usuario
CREATE TABLE jobs_usuario (
  id NUMBER PRIMARY KEY,
  password VARCHAR2(128) NOT NULL,
  last_login TIMESTAMP,
  is_superuser NUMBER(1) DEFAULT 0 NOT NULL,
  username VARCHAR2(150) NOT NULL UNIQUE,
  first_name VARCHAR2(150),
  last_name VARCHAR2(150),
  email VARCHAR2(254) NOT NULL,
  is_staff NUMBER(1) DEFAULT 0 NOT NULL,
  is_active NUMBER(1) DEFAULT 1 NOT NULL,
  date_joined TIMESTAMP NOT NULL,
  telefono VARCHAR2(20),
  direccion CLOB,
  fecha_nacimiento DATE,
  es_prestador NUMBER(1) DEFAULT 0 NOT NULL
);

-- Tabla de grupos de usuarios (necesaria para el modelo de usuarios de Django)
CREATE TABLE auth_group (
  id NUMBER PRIMARY KEY,
  name VARCHAR2(150) NOT NULL UNIQUE
);

-- Tabla de permisos (necesaria para el modelo de usuarios de Django)
CREATE TABLE auth_permission (
  id NUMBER PRIMARY KEY,
  name VARCHAR2(255) NOT NULL,
  content_type_id NUMBER NOT NULL,
  codename VARCHAR2(100) NOT NULL
);

-- Tabla de permisos de usuario (necesaria para el modelo de usuarios de Django)
CREATE TABLE jobs_usuario_user_permissions (
  id NUMBER PRIMARY KEY,
  usuario_id NUMBER NOT NULL,
  permission_id NUMBER NOT NULL,
  CONSTRAINT jobs_usuario_user_perm_usuario_id_fk FOREIGN KEY (usuario_id) REFERENCES jobs_usuario (id),
  CONSTRAINT jobs_usuario_user_perm_permission_id_fk FOREIGN KEY (permission_id) REFERENCES auth_permission (id),
  CONSTRAINT jobs_usuario_user_perm_unique UNIQUE (usuario_id, permission_id)
);

-- Tabla de grupos de usuario (necesaria para el modelo de usuarios de Django)
CREATE TABLE jobs_usuario_groups (
  id NUMBER PRIMARY KEY,
  usuario_id NUMBER NOT NULL,
  group_id NUMBER NOT NULL,
  CONSTRAINT jobs_usuario_groups_usuario_id_fk FOREIGN KEY (usuario_id) REFERENCES jobs_usuario (id),
  CONSTRAINT jobs_usuario_groups_group_id_fk FOREIGN KEY (group_id) REFERENCES auth_group (id),
  CONSTRAINT jobs_usuario_groups_unique UNIQUE (usuario_id, group_id)
);

-- Tabla de Profesión
CREATE TABLE jobs_profesion (
  id NUMBER PRIMARY KEY,
  nombre VARCHAR2(100) NOT NULL,
  descripcion CLOB
);

-- Tabla de Servicio
CREATE TABLE jobs_servicio (
  id NUMBER PRIMARY KEY,
  tipo_servicio VARCHAR2(100) NOT NULL,
  descripcion CLOB NOT NULL,
  tarifa NUMBER(10,2) NOT NULL,
  activo NUMBER(1) DEFAULT 1 NOT NULL,
  fecha_creacion TIMESTAMP NOT NULL,
  prestador_id NUMBER NOT NULL,
  profesion_id NUMBER NOT NULL,
  CONSTRAINT jobs_servicio_prestador_id_fk FOREIGN KEY (prestador_id) REFERENCES jobs_usuario (id),
  CONSTRAINT jobs_servicio_profesion_id_fk FOREIGN KEY (profesion_id) REFERENCES jobs_profesion (id)
);

-- Tabla de Trabajo
CREATE TABLE jobs_trabajo (
  id NUMBER PRIMARY KEY,
  fecha_solicitud TIMESTAMP NOT NULL,
  fecha_trabajo TIMESTAMP,
  estado VARCHAR2(20) NOT NULL,
  servicio_id NUMBER NOT NULL,
  cliente_id NUMBER NOT NULL,
  CONSTRAINT jobs_trabajo_servicio_id_fk FOREIGN KEY (servicio_id) REFERENCES jobs_servicio (id),
  CONSTRAINT jobs_trabajo_cliente_id_fk FOREIGN KEY (cliente_id) REFERENCES jobs_usuario (id)
);

-- Tabla de Valoración
CREATE TABLE jobs_valoracion (
  id NUMBER PRIMARY KEY,
  puntuacion NUMBER(1) NOT NULL,
  comentario CLOB,
  fecha TIMESTAMP NOT NULL,
  trabajo_id NUMBER NOT NULL,
  CONSTRAINT jobs_valoracion_trabajo_id_fk FOREIGN KEY (trabajo_id) REFERENCES jobs_trabajo (id),
  CONSTRAINT jobs_valoracion_trabajo_id_unique UNIQUE (trabajo_id)
);