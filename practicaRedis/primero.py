import redis
import json

# Conexión a Redis
conexionRedis = redis.ConnectionPool(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)

baseDatosRedis = redis.Redis(connection_pool=conexionRedis)

#1 - Crear registros clave-valor(0.25 puntos)

#Registro actividad en plataforma web
baseDatosRedis.set('actividad:est001', 'Acceso a plataforma', ex=900)
baseDatosRedis.set('actividad:est001:tiempo', 35)

baseDatosRedis.set('actividad:est002', 'Envió tarea', ex=900)
baseDatosRedis.set('actividad:est002:tiempo', 48)

baseDatosRedis.set('actividad:est003', 'Acceso al módulo de Matemáticas', ex=900)
baseDatosRedis.set('actividad:est003:tiempo', 78)

baseDatosRedis.set('actividad:est004', 'Acceso al módulo de Matemáticas', ex=900)
baseDatosRedis.set('actividad:est004:tiempo', 12)

baseDatosRedis.set('actividad:est005', 'Acceso al módulo de Química', ex=900)
baseDatosRedis.set('actividad:est005:tiempo', 125)

baseDatosRedis.set('actividad:est006', 'Acceso a los ajustes del perfil ', ex=900)
baseDatosRedis.set('actividad:est006:tiempo', 34)


#Estado de tutorías en la plataforma
baseDatosRedis.set('tutoria:sesion101', 'En progreso', ex=300)
baseDatosRedis.set('tutoria:sesion101:tutor', 'Jorge Agustín')

baseDatosRedis.set('tutoria:sesion102', 'Finalizada', ex=300)
baseDatosRedis.set('tutoria:sesion102:tutor', 'José Antonio')

baseDatosRedis.set('tutoria:sesion103', 'Finalizada', ex=300)
baseDatosRedis.set('tutoria:sesion103:tutor', 'José Antonio')

#Otros datos de la plataforma
baseDatosRedis.set('profesor:ultimaconexion:prof001', '2025-11-18 10:56:02')
baseDatosRedis.set('profesor:ultimaconexion:prof002', '2025-11-19 20:00:12')
baseDatosRedis.set('profesor:ultimaconexion:prof003', '2025-11-19 17:03:21')
baseDatosRedis.set('profesor:ultimaconexion:prof004', '2025-11-20 16:23:51')
baseDatosRedis.set('profesor:ultimaconexion:prof012', '2025-11-19 11:23:51')

valor = baseDatosRedis.get('actividad:est001')
print(valor)

#2 - Obtener y mostrar el número de claves registradas (0.25 puntos)

claves = baseDatosRedis.keys()

for clave in claves:
	print('Clave:', clave , ' y Valor: ', baseDatosRedis.get(clave))

#3 - Obtener y mostrar un registro en base a una clave (0.25 puntos)

clave = 'actividad:est001'
valor = baseDatosRedis.get(clave)

print(f"El valor en la clave '{clave}' es: '{valor}'")

#4 - Actualizar el valor de una clave y mostrar el nuevo valor(0.25 puntos)

nuevo_valor = 'Ingreso a módulo de Física'
valor_actualizado = baseDatosRedis.get(clave)

print(f"El nuevo valor en la clave '{clave}' es: '{valor}'")

#5 - Eliminar una clave-valor y mostrar la clave y el valor eliminado(0.25 puntos)

claveBorrar = 'actividad:est006'
valor_eliminado = baseDatosRedis.get(claveBorrar)
baseDatosRedis.delete(claveBorrar)

print(f"La clave '{claveBorrar}' y su valor '{valor_eliminado}' han sido eliminadas")

#6 - Obtener y mostrar todas las claves guardadas (0.25 puntos)

claves = baseDatosRedis.keys()

for clave in claves:
	print('Clave:', clave)

#7 - Obtener y mostrar todos los valores guardados(0.25 puntos)

for clave in claves:
	print('Valor: ', baseDatosRedis.get(clave))

#8 - Obtener y mostrar varios registros con una clave con un patrón en común usando * (0.5 puntos)

# Claves de estudiantes sacandolos de la clave 'actividad' 
claves_actividad = baseDatosRedis.keys('actividad:*')

print("\n#8 - Registros con patrón '*' (actividad:*)")
for clave in claves_actividad:
    print(f"{clave} --> {baseDatosRedis.get(clave)}")

#9 - Obtener y mostrar varios registros con una clave con un patrón en común usando [] (0.5 puntos)

# Claves que contengan actividad:est00[1-5]

claves_rango = baseDatosRedis.keys('actividad:est00[1-5]')

print("\n#9 - Registros con patrón '[]' (actividad:est00[1-5])")
for clave in claves_rango:
    print(f"{clave} --> {baseDatosRedis.get(clave)}")

#10 - Obtener y mostrar varios registros con una clave con un patrón en común usando ? (0.5 puntos)

claves_comodin = baseDatosRedis.keys('profesor:ultimaconexion:prof00?')

print("\n#10 - Registros con patrón '?' (profesor:ultimaconexion:prof00?)")
for clave in claves_comodin:
    print(f"{clave} --> {baseDatosRedis.get(clave)}")

#11 - Obtener y mostrar varios registros y filtrarlos por un valor en concreto. (0.5 puntos)

# Filtrar todas las tutorías que están 'Finalizada'
claves_tutorias = baseDatosRedis.keys('tutoria:*')

print("\n#11 - Registros filtrados por valor 'Finalizada'")
for clave in claves_tutorias:
    valor = baseDatosRedis.get(clave)
    if valor == 'Finalizada':
        print(f"{clave} --> {valor}")

#12 - Actualizar una serie de registros en base a un filtro (por ejemplo aumentar su valor en 1 )(0.5 puntos)

print("\n#12 - Aumentar tiempo de actividad en 10 minutos")

claves_tiempo = baseDatosRedis.keys('actividad:*:tiempo')

for clave in claves_tiempo:
    valor_actual = baseDatosRedis.get(clave)
    
    if valor_actual is not None:
        # Convertir a entero y sumar 10
        nuevo_valor = int(valor_actual) + 10
        baseDatosRedis.set(clave, nuevo_valor)
        print(f"{clave} actualizado: {valor_actual} --> {nuevo_valor}")

#13 - Eliminar una serie de registros en base a un filtro (0.5 puntos)

print("\n#13 - Eliminar todas las claves de tiempo de actividad")

claves_tiempo = baseDatosRedis.keys('actividad:*:tiempo')

for clave in claves_tiempo:
    valor = baseDatosRedis.get(clave)
    baseDatosRedis.delete(clave)
    print(f"Clave eliminada: {clave} --> Valor eliminado: {valor}")

#14

# Crear registros individuales por estudiante
baseDatosRedis.json().set("usuarios:est001", "$", {"id": "est001", "actividad": "Acceso a plataforma", "tiempo": 35})
baseDatosRedis.json().set("usuarios:est002", "$", {"id": "est002", "actividad": "Envió tarea", "tiempo": 48})
baseDatosRedis.json().set("usuarios:est003", "$", {"id": "est003", "actividad": "Acceso al módulo de Matemáticas", "tiempo": 78})
baseDatosRedis.json().set("usuarios:est004", "$", {"id": "est004", "actividad": "Acceso al módulo de Matemáticas", "tiempo": 12})
baseDatosRedis.json().set("usuarios:est005", "$", {"id": "est005", "actividad": "Acceso al módulo de Química", "tiempo": 125})

# Crear un array vacío en Redis
baseDatosRedis.json().set("json_estudiantes", "$", [])

# Agregar los registros al array usando arrappend
for i in range(1, 6):
    estudiante = baseDatosRedis.json().get(f"usuarios:est00{i}")
    baseDatosRedis.json().arrappend("json_estudiantes", "$", estudiante)

# Mostrar el array final en pantalla
json_array = baseDatosRedis.json().get("json_estudiantes")
print("#14 - Estructura JSON generada a partir de Redis:")
print(json_array)

#15



#16 - Crear una lista en Redis (0.25 puntos)
#17 - Obtener elementos de una lista con un filtro en concreto(0.5 puntos)

baseDatosRedis.close()