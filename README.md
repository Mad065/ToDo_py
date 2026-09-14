# ToDo_py - Lista de Tareas

Una aplicación web sencilla, rápida y elegante para la gestión de tareas pendientes, desarrollada con **Python**, **Flask** y **SQLite**.

---

## 🚀 Características

- **Gestión de tareas:** Agrega nuevas tareas y márcalas como completadas con un solo clic.
- **Persistencia de datos:** Base de datos relacional ligera con SQLite (`todo.db`), sin necesidad de configurar servidores de base de datos externos.
- **Contador en tiempo real:** Muestra dinámicamente el número de tareas pendientes.
- **Interfaz limpia y moderna:** Diseño minimalista, responsivo y adaptado para dispositivos móviles y escritorio.

---

## 🛠️ Tecnologías Utilizadas

- **Backend:** Python 3, [Flask](https://flask.palletsprojects.com/) (3.1.x)
- **Base de datos:** SQLite3
- **Frontend:** HTML5, CSS3 (Vanilla)

---

## 📁 Estructura del Proyecto

```text
ToDo_py/
├── app.py              # Controlador principal y rutas de la aplicación Flask
├── db.py               # Gestión de la base de datos SQLite y consultas SQL
├── requirements.txt    # Dependencias de Python
├── static/
│   └── style.css       # Hoja de estilos de la interfaz
├── templates/
│   └── index.html      # Plantilla principal renderizada con Jinja2
├── todo.db             # Archivo de base de datos SQLite (se genera automáticamente)
└── README.md           # Documentación del proyecto
```

---

## ⚙️ Instalación y Configuración

Sigue estos pasos para ejecutar el proyecto en tu entorno local:

### 1. Clonar el repositorio o ingresar al directorio

```bash
cd ToDo_py
```

### 2. Crear y activar un entorno virtual

- En **macOS / Linux**:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

- En **Windows**:
  ```bash
  python -m venv .venv
  .venv\Scripts\activate
  ```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

---

## ▶️ Ejecución

Para iniciar el servidor de desarrollo, ejecuta:

```bash
python app.py
```

Una vez iniciado, abre tu navegador web y accede a:

👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 📌 Rutas Disponibles

| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| `GET` | `/` | Vista principal con la lista de tareas y contador de pendientes |
| `POST` | `/tasks` | Crea y guarda una nueva tarea |
| `POST` | `/tasks/<id>/complete` | Marca la tarea especificada como completada |

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Siéntete libre de utilizarlo y modificarlo según tus necesidades.
