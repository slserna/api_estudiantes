from flask import Flask, request, jsonify
import sqlite3
import os

# ============================================================
# INICIALIZACIÓN DE LA APLICACIÓN FLASK
# ============================================================
app = Flask(__name__)

# Ruta de la base de datos SQLite
DB_PATH = "estudiantes.db"


# ============================================================
# FUNCIÓN AUXILIAR: Conexión a la base de datos
# ============================================================
def get_db_connection():
    """
    Crea y devuelve una conexión a la base de datos SQLite.
    row_factory permite acceder a las columnas por nombre (como un diccionario).
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Acceso tipo dict: fila["nombre"]
    return conn


# ============================================================
# FUNCIÓN AUXILIAR: Crear la tabla si no existe
# ============================================================
def init_db():
    """
    Inicializa la base de datos creando la tabla 'estudiantes'
    si aún no existe. Se ejecuta una sola vez al iniciar el servidor.
    """
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS estudiantes (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre    TEXT    NOT NULL,
            carrera   TEXT    NOT NULL,
            semestre  INTEGER NOT NULL,
            creado_en DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    print("✅ Base de datos lista.")


# ============================================================
# ENDPOINT GET /estudiantes
# Devuelve todos los estudiantes registrados
# ============================================================
@app.route("/estudiantes", methods=["GET"])
def obtener_estudiantes():
    """
    GET /estudiantes
    Consulta y devuelve todos los estudiantes en la base de datos.

    Respuesta exitosa (200):
    {
        "total": 2,
        "estudiantes": [
            { "id": 1, "nombre": "Ana López", "carrera": "Ingeniería", "semestre": 3, "creado_en": "..." },
            ...
        ]
    }
    """
    conn = get_db_connection()

    # Ejecutamos una consulta SELECT para traer todos los registros
    filas = conn.execute(
        "SELECT id, nombre, carrera, semestre, creado_en FROM estudiantes ORDER BY id ASC"
    ).fetchall()

    conn.close()

    # Convertimos cada fila (sqlite3.Row) a un diccionario Python
    estudiantes = [dict(fila) for fila in filas]

    return jsonify({
        "total": len(estudiantes),
        "estudiantes": estudiantes
    }), 200


# ============================================================
# ENDPOINT POST /estudiantes
# Registra un nuevo estudiante
# ============================================================
@app.route("/estudiantes", methods=["POST"])
def agregar_estudiante():
    """
    POST /estudiantes
    Recibe un JSON con los datos del estudiante y lo guarda en la BD.

    Cuerpo esperado (JSON):
    {
        "nombre":   "Ana López",
        "carrera":  "Ingeniería en Sistemas",
        "semestre": 3
    }

    Respuesta exitosa (201):
    {
        "mensaje": "Estudiante registrado correctamente.",
        "estudiante": { "id": 1, "nombre": "Ana López", ... }
    }

    Respuesta de error (400):
    {
        "error": "El campo 'nombre' es obligatorio."
    }
    """

    # 1. Leer el JSON enviado en el cuerpo de la petición
    datos = request.get_json()

    # 2. Validar que el cuerpo no esté vacío
    if not datos:
        return jsonify({"error": "Se esperaba un cuerpo JSON."}), 400

    # 3. Validar campos obligatorios
    campos_requeridos = ["nombre", "carrera", "semestre"]
    for campo in campos_requeridos:
        if campo not in datos or str(datos[campo]).strip() == "":
            return jsonify({"error": f"El campo '{campo}' es obligatorio."}), 400

    # 4. Validar que semestre sea un número entero positivo
    try:
        semestre = int(datos["semestre"])
        if semestre < 1 or semestre > 12:
            return jsonify({"error": "El semestre debe ser un número entre 1 y 12."}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "El campo 'semestre' debe ser un número entero."}), 400

    nombre  = datos["nombre"].strip()
    carrera = datos["carrera"].strip()

    # 5. Insertar el nuevo registro en la base de datos
    conn = get_db_connection()
    cursor = conn.execute(
        "INSERT INTO estudiantes (nombre, carrera, semestre) VALUES (?, ?, ?)",
        (nombre, carrera, semestre)   # ← Parámetros ? evitan SQL Injection
    )
    conn.commit()

    # 6. Recuperar el registro recién insertado para devolverlo en la respuesta
    nuevo_id = cursor.lastrowid
    fila = conn.execute(
        "SELECT id, nombre, carrera, semestre, creado_en FROM estudiantes WHERE id = ?",
        (nuevo_id,)
    ).fetchone()
    conn.close()

    return jsonify({
        "mensaje": "Estudiante registrado correctamente.",
        "estudiante": dict(fila)
    }), 201


# ============================================================
# ENDPOINT GET /estudiantes/<id>
# Devuelve un estudiante específico por su ID
# ============================================================
@app.route("/estudiantes/<int:id>", methods=["GET"])
def obtener_estudiante(id):
    """
    GET /estudiantes/<id>
    Devuelve los datos de un estudiante específico.
    """
    conn = get_db_connection()
    fila = conn.execute(
        "SELECT id, nombre, carrera, semestre, creado_en FROM estudiantes WHERE id = ?",
        (id,)
    ).fetchone()
    conn.close()

    if fila is None:
        return jsonify({"error": f"No se encontró un estudiante con id={id}."}), 404

    return jsonify(dict(fila)), 200


# ============================================================
# PUNTO DE ENTRADA
# ============================================================
if __name__ == "__main__":
    init_db()          # Crear la tabla si no existe
    app.run(debug=True, port=5000)
