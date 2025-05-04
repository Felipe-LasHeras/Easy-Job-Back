-- Insertar profesiones iniciales
INSERT INTO jobs_profesion (id, nombre, descripcion) VALUES (jobs_profesion_seq.NEXTVAL, 'Programador', 'Desarrollo de aplicaciones web y móviles utilizando tecnologías HTML, CSS, JavaScript, React y Node.js. Experiencia en bases de datos SQL y NoSQL.');
INSERT INTO jobs_profesion (id, nombre, descripcion) VALUES (jobs_profesion_seq.NEXTVAL, 'Diseñador', 'Diseño gráfico, web y publicitario. Manejo de herramientas Adobe y experiencia en UI/UX.');
INSERT INTO jobs_profesion (id, nombre, descripcion) VALUES (jobs_profesion_seq.NEXTVAL, 'Contador', 'Servicios contables y tributarios. Declaración de impuestos, contabilidad para empresas y personas.');
INSERT INTO jobs_profesion (id, nombre, descripcion) VALUES (jobs_profesion_seq.NEXTVAL, 'Abogado', 'Asesoría legal en diversas áreas como civil, laboral, comercial y tributario.');
INSERT INTO jobs_profesion (id, nombre, descripcion) VALUES (jobs_profesion_seq.NEXTVAL, 'Electricista', 'Instalaciones eléctricas domiciliarias e industriales. Reparaciones y mantenimiento.');

-- Insertar usuario administrador
INSERT INTO jobs_usuario (
  id, 
  password,
  is_superuser,
  username,
  first_name,
  last_name,
  email,
  is_staff,
  is_active,
  date_joined,
  es_prestador
) VALUES (
  jobs_usuario_seq.NEXTVAL,
  'pbkdf2_sha256$600000$adminpassword123456789abcdef$dUuUATuFhzLBR8Q9E5ZIZ5lOw/Z5e5vKwM0XpH2nwj0=', -- Contraseña: admin123
  1,
  'admin',
  'Administrador',
  'Sistema',
  'admin@easyjob.com',
  1,
  1,
  CURRENT_TIMESTAMP,
  0
);

COMMIT;