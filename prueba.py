import re
import requests
import sqlite3

from colorama import Fore

# Realizar la solicitud al sitio web
website = "https://www.vulnhub.com/"
resultado = requests.get(website)
content = resultado.text

# Encontrar todas las máquinas en el sitio web
patron = r"/entry/[\w-]*"
maquinas_repetidas = re.findall(patron, str(content))
sin_duplicados = list(set(maquinas_repetidas))

# Crear una lista para almacenar los nombres de las máquinas
maquinas_final = []

# Iterar sobre las máquinas encontradas
for i in sin_duplicados:
    nombre_maquinas = i.replace("/entry/", "")
    maquinas_final.append(nombre_maquinas)
    print(nombre_maquinas)

# Conectar a la base de datos SQLite (esto creará la base de datos si no existe)
conn = sqlite3.connect('maquinas.db')
cursor = conn.cursor()

# Crear una tabla si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS maquinas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT
    )
''')
conn.commit()

# Insertar nombres de máquinas en la base de datos
for nombre_maquina in maquinas_final:
    cursor.execute('INSERT INTO maquinas (nombre) VALUES (?)', (nombre_maquina,))
conn.commit()

# Cerrar la conexión a la base de datos
conn.close()

# Verificar si la máquina 'noob-1' existe en la base de datos
maquina_noob = "watermarked"
conn = sqlite3.connect('maquinas.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM maquinas WHERE nombre = ?', (maquina_noob,))
result = cursor.fetchone()
conn.close()

if result:
    print(f"'{maquina_noob}' ya existe en la base de datos.")
else:
    print(f"'{maquina_noob}' es una máquina nueva y se agregó a la base de datos.")


