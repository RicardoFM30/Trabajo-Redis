-- Script creación base de datos Postgres --

DROP TABLE IF EXISTS Recomendaciones;
DROP TABLE IF EXISTS Retroalimentaciones;
DROP TABLE IF EXISTS PerfilesTalento;
DROP TABLE IF EXISTS Proyectos;
DROP TABLE IF EXISTS Tutorias;
DROP TABLE IF EXISTS Participaciones;
DROP TABLE IF EXISTS Actividades;
DROP TABLE IF EXISTS HabilidadesBlandas;
DROP TABLE IF EXISTS Calificaciones;
DROP TABLE IF EXISTS Asignaturas;
DROP TABLE IF EXISTS Profesores;
DROP TABLE IF EXISTS Estudiantes;

CREATE TABLE Estudiantes (
  id_estudiante SERIAL PRIMARY KEY,
  nombre VARCHAR(100),
  apellidos VARCHAR(100),
  edad INT,
  curso VARCHAR(20),
  grupo VARCHAR(10),
  email VARCHAR(100),
  telefono VARCHAR(20)
);

CREATE TABLE Profesores (
  id_profesor SERIAL PRIMARY KEY,
  nombre VARCHAR(100),
  apellidos VARCHAR(100),
  email VARCHAR(100),
  telefono VARCHAR(20),
  materia VARCHAR(100)
);

CREATE TABLE Asignaturas (
  id_asignatura SERIAL PRIMARY KEY,
  nombre VARCHAR(100),
  descripcion TEXT,
  curso VARCHAR(20),
  id_profesor INT REFERENCES Profesores(id_profesor)
);

CREATE TABLE Calificaciones (
  id_calificacion SERIAL PRIMARY KEY,
  id_estudiante INT REFERENCES Estudiantes(id_estudiante),
  nota DECIMAL(5,2),
  id_asignatura INT REFERENCES Asignaturas(id_asignatura),
  fecha_evaluacion DATE,
  asistencia BOOLEAN
);

CREATE TABLE HabilidadesBlandas (
  id_habilidad SERIAL PRIMARY KEY,
  id_estudiante INT REFERENCES Estudiantes(id_estudiante),
  habilidad VARCHAR(100),
  puntuacion DECIMAL(5,2),
  fecha_registro DATE
);

CREATE TABLE Actividades (
  id_actividad SERIAL PRIMARY KEY,
  nombre VARCHAR(100),
  tipo VARCHAR(50),
  fecha_inicio DATE,
  fecha_fin DATE,
  descripcion TEXT
);

CREATE TABLE Participaciones (
  id_participacion SERIAL PRIMARY KEY,
  id_estudiante INT REFERENCES Estudiantes(id_estudiante),
  id_actividad INT REFERENCES Actividades(id_actividad),
  rol VARCHAR(50),
  fecha_participacion DATE,
  horas_dedicadas INT,
  resultado VARCHAR(100)
);

CREATE TABLE Tutorias (
  id_tutoria SERIAL PRIMARY KEY,
  id_estudiante INT REFERENCES Estudiantes(id_estudiante),
  id_profesor INT REFERENCES Profesores(id_profesor),
  fecha DATE,
  tema VARCHAR(100),
  observaciones TEXT
);

CREATE TABLE Proyectos (
  id_proyecto SERIAL PRIMARY KEY,
  id_estudiante INT REFERENCES Estudiantes(id_estudiante),
  nombre VARCHAR(100),
  descripcion TEXT,
  fecha_entrega DATE,
  calificacion_final DECIMAL(5,2),
  evaluador INT REFERENCES Profesores(id_profesor),
  material_adjunto VARCHAR(255)
);

CREATE TABLE PerfilesTalento (
  id_perfil SERIAL PRIMARY KEY,
  id_estudiante INT UNIQUE REFERENCES Estudiantes(id_estudiante),
  promedio_general DECIMAL(5,2),
  habilidades_destacadas TEXT,
  intereses TEXT,
  fortalezas TEXT,
  recomendaciones_generadas TEXT
);

CREATE TABLE Retroalimentaciones (
  id_feedback SERIAL PRIMARY KEY,
  id_estudiante INT REFERENCES Estudiantes(id_estudiante),
  autor_feedback VARCHAR(100),
  tipo_feedback VARCHAR(50),
  comentario TEXT,
  fecha DATE
);

CREATE TABLE Recomendaciones (
  id_recomendacion SERIAL PRIMARY KEY,
  id_estudiante INT REFERENCES Estudiantes(id_estudiante),
  tipo VARCHAR(50),
  detalle TEXT,
  fecha_generacion DATE
);


-----------------------------------------------------
-- DATOS DE EJEMPLO
-----------------------------------------------------

-- Profesores
INSERT INTO Profesores (nombre, apellidos, email, telefono, materia) VALUES
('Carlos', 'Ramírez', 'carlos.ramirez@colegio.com', '600100200', 'Matemáticas'),
('Laura', 'Sánchez', 'laura.sanchez@colegio.com', '600300400', 'Lengua'),
('Miguel', 'Torres', 'miguel.torres@colegio.com', '600500600', 'Ciencias');

-- Estudiantes
INSERT INTO Estudiantes (nombre, apellidos, edad, curso, grupo, email, telefono) VALUES
('Ana', 'López', 15, '4ESO', 'A', 'ana.lopez@estudiantes.com', '611111111'),
('Javier', 'Martín', 16, '4ESO', 'B', 'javier.martin@estudiantes.com', '622222222'),
('María', 'Gómez', 15, '4ESO', 'A', 'maria.gomez@estudiantes.com', '633333333');

-- Asignaturas
INSERT INTO Asignaturas (nombre, descripcion, curso, id_profesor) VALUES
('Matemáticas I', 'Álgebra, ecuaciones y trigonometría', '4ESO', 1),
('Lengua y Literatura', 'Gramática y análisis de textos', '4ESO', 2),
('Biología', 'Estudio del cuerpo humano y ecosistemas', '4ESO', 3);

-- Calificaciones
INSERT INTO Calificaciones (id_estudiante, id_asignatura, nota, fecha_evaluacion, asistencia) VALUES
(1, 1, 8.5, '2024-01-10', TRUE),
(1, 2, 9.2, '2024-01-12', TRUE),
(2, 1, 6.8, '2024-01-11', FALSE),
(3, 3, 7.9, '2024-01-15', TRUE);

-- Habilidades blandas
INSERT INTO HabilidadesBlandas (id_estudiante, habilidad, puntuacion, fecha_registro) VALUES
(1, 'Trabajo en equipo', 8.0, '2024-02-01'),
(2, 'Comunicación', 7.5, '2024-02-01'),
(3, 'Liderazgo', 9.0, '2024-02-01');
