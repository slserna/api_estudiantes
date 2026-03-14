# 📚 API de Estudiantes — Flask + SQLite

Proyecto educativo que enseña a conectar **Flask** con una **base de datos SQLite**
y realizar operaciones básicas de almacenamiento y consulta.

---

## 🗂️ Estructura del proyecto

```
api_estudiantes/
├── app.py            ← Código principal de la API
├── requirements.txt  ← Dependencias de Python
├── README.md         ← Este archivo
└── estudiantes.db    ← Base de datos (se crea automáticamente)
```

---

## ⚙️ Instalación y ejecución

### 1. Crear entorno virtual (recomendado)
```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar el servidor
```bash
python app.py
```

El servidor correrá en: **http://127.0.0.1:5000**

---

## 🔌 Endpoints disponibles

### `POST /estudiantes` — Registrar un estudiante

**Cuerpo de la petición (JSON):**
```json
{
  "nombre":   "Ana López",
  "carrera":  "Ingeniería en Sistemas",
  "semestre": 3
}
```

**Respuesta exitosa `201 Created`:**
```json
{
  "mensaje": "Estudiante registrado correctamente.",
  "estudiante": {
    "id": 1,
    "nombre": "Ana López",
    "carrera": "Ingeniería en Sistemas",
    "semestre": 3,
    "creado_en": "2025-01-15 10:30:00"
  }
}
```

**Error `400 Bad Request`** (campo faltante):
```json
{ "error": "El campo 'nombre' es obligatorio." }
```

---

### `GET /estudiantes` — Consultar todos los estudiantes

**Respuesta exitosa `200 OK`:**
```json
{
  "total": 2,
  "estudiantes": [
    { "id": 1, "nombre": "Ana López",  "carrera": "Ing. en Sistemas", "semestre": 3, "creado_en": "..." },
    { "id": 2, "nombre": "Carlos Ruiz", "carrera": "Contabilidad",     "semestre": 5, "creado_en": "..." }
  ]
}
```

---

### `GET /estudiantes/<id>` — Consultar un estudiante por ID

```
GET /estudiantes/1
```

**Respuesta exitosa `200 OK`:**
```json
{ "id": 1, "nombre": "Ana López", "carrera": "Ing. en Sistemas", "semestre": 3, "creado_en": "..." }
```

**Error `404 Not Found`:**
```json
{ "error": "No se encontró un estudiante con id=99." }
```

---

## 🧪 Ejemplos con curl

```bash
# Registrar un estudiante
curl -X POST http://127.0.0.1:5000/estudiantes \
     -H "Content-Type: application/json" \
     -d '{"nombre": "Ana López", "carrera": "Ing. en Sistemas", "semestre": 3}'

# Consultar todos
curl http://127.0.0.1:5000/estudiantes

# Consultar por ID
curl http://127.0.0.1:5000/estudiantes/1
```

---

## 🧠 Conceptos que aprenderás

| Concepto | Dónde se aplica |
|---|---|
| Rutas Flask (`@app.route`) | Cada endpoint definido |
| Métodos HTTP (GET / POST) | `methods=["GET"]`, `methods=["POST"]` |
| Leer JSON del request | `request.get_json()` |
| Conexión SQLite | `sqlite3.connect(DB_PATH)` |
| Consultas parametrizadas | `conn.execute("... WHERE id = ?", (id,))` |
| Respuestas JSON | `jsonify({...})` |
| Códigos de estado HTTP | `200`, `201`, `400`, `404` |

---

## 🛡️ Buenas prácticas incluidas

- ✅ **Parámetros `?`** en SQL → previene inyección SQL
- ✅ **Validación de campos** antes de insertar
- ✅ **Códigos HTTP correctos** (201 para creación, 404 para no encontrado)
- ✅ **`row_factory`** para acceder a columnas por nombre
- ✅ **Cierre de conexión** después de cada operación
