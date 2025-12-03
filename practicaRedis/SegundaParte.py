import psycopg2
import redis
import json

# Conexión postgre
pg = psycopg2.connect(
    host="localhost",
    user="usuario",
    password="usuario123",
    database="proyecto",
    port=5432
)
cursor = pg.cursor()

# Conexión redis
r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

print("\n====================")
print(" #21 - SQL → REDIS")
print("====================\n")

# Importar estudiantes con consultas
print("Importando tabla ESTUDIANTES...\n")

cursor.execute("""
    SELECT id_estudiante, nombre, apellidos, edad, curso, grupo, email, telefono
    FROM Estudiantes
""")
rows = cursor.fetchall()

for row in rows:
    id_est, nombre, apellidos, edad, curso, grupo, email, telefono = row

    key = f"sql:estudiante:{id_est}"
    data = {
        "id_estudiante": id_est,
        "nombre": nombre,
        "apellidos": apellidos,
        "edad": edad,
        "curso": curso,
        "grupo": grupo,
        "email": email,
        "telefono": telefono
    }

    # Guardar como string JSON
    r.set(key, json.dumps(data))
    
    # Leer de Redis y mostrar por pantalla
    datos_estudiantes = json.loads(r.get(key))
    print(f"✔ Importado → {key} → {datos_estudiantes}")

# Se sigue la misma dinámica para profesores y las asignaturas
print("\nImportando tabla PROFESORES...\n")

cursor.execute("""
    SELECT id_profesor, nombre, apellidos, email, telefono, materia
    FROM Profesores
""")
rows = cursor.fetchall()

for row in rows:
    id_prof, nombre, apellidos, email, telefono, materia = row

    key = f"sql:profesor:{id_prof}"
    data = {
        "id_profesor": id_prof,
        "nombre": nombre,
        "apellidos": apellidos,
        "email": email,
        "telefono": telefono,
        "materia": materia
    }

    r.set(key, json.dumps(data))
    
    datos_profesores = json.loads(r.get(key))
    print(f"✔ Importado → {key} → {datos_profesores}")

print("\nImportando tabla ASIGNATURAS...\n")

cursor.execute("""
    SELECT id_asignatura, nombre, descripcion, curso, id_profesor
    FROM Asignaturas
""")
rows = cursor.fetchall()

for row in rows:
    id_asig, nombre, descripcion, curso, id_prof = row

    key = f"sql:asignatura:{id_asig}"
    data = {
        "id_asignatura": id_asig,
        "nombre": nombre,
        "descripcion": descripcion,
        "curso": curso,
        "id_profesor": id_prof
    }

    r.set(key, json.dumps(data))
    
    datos_asignaturas = json.loads(r.get(key))
    print(f"✔ Importado → {key} → {datos_asignaturas}")


print("\n====================")
print(" #22 - REDIS → SQL")
print("====================\n")

# Tan solo voy a importar datos de estudiantes a postgres guardados en redis

estudiantes = [
    {"nombre": "Ricardo", "apellidos": "Martínez", "edad": 16, "curso": "CEBDIA", "grupo": "A", "email": "lucia@mail.com", "telefono": "600111222"},
    {"nombre": "Fausto", "apellidos": "Gómez", "edad": 17, "curso": "CEBDIA", "grupo": "B", "email": "carlos@mail.com", "telefono": "600333444"},
    {"nombre": "Viktor", "apellidos": "Rodríguez", "edad": 15, "curso": "CEBDIA", "grupo": "C", "email": "elena@mail.com", "telefono": "600555666"}
]

for i, est in enumerate(estudiantes, start=1):
    key = f"estudiantesNuevos:{i}"
    r.set(key, json.dumps(est))

for key in r.keys("estudiantesNuevos:*"):
    data = json.loads(r.get(key))

    cursor.execute("""
        INSERT INTO Estudiantes (nombre, apellidos, edad, curso, grupo, email, telefono)
        VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id_estudiante
    """, (
        data["nombre"],
        data["apellidos"],
        data["edad"],
        data["curso"],
        data["grupo"],
        data["email"],
        data["telefono"]
    ))
    id_est = cursor.fetchone()[0]
    pg.commit()
    print(f"✔ Importado a Postgres → {key} → id_estudiante={id_est} → {data}")

cursor.close()
pg.close()
