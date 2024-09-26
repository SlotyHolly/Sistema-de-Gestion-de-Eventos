# Sistema de Gestión de Eventos

Este proyecto es un **Sistema de Gestión de Eventos** desarrollado en **Python 3.11** con **Tkinter** para la interfaz gráfica de usuario (GUI) y **JSON** como base de datos para almacenar la información de usuarios y eventos. El sistema permite la gestión de eventos para **usuarios** y **administradores**, con funciones de autenticación, compra de tickets y manejo de eventos.

## Características principales
- **Login y Registro**:
  - Los usuarios pueden iniciar sesión con sus credenciales.
  - Los nuevos usuarios pueden registrarse con un nombre de usuario y contraseña.
  - Los administradores y usuarios tienen roles separados.
  
- **Dashboard del Usuario**:
  - Los usuarios pueden ver y comprar tickets de eventos.
  - Visualización de los tickets adquiridos.
  
- **Dashboard del Administrador**:
  - Los administradores pueden cargar nuevos eventos.
  - Los administradores pueden modificar los eventos existentes.
  - Se muestra un resumen de los eventos activos con la opción de cargar flyers.
  
- **Recuperación de Contraseña**:
  - Los usuarios pueden recuperar su contraseña mediante un código predefinido ("1234").
  - Validación del código y cambio de contraseña.

## Tecnologías usadas
- **Python 3.11**: Lenguaje de programación principal.
- **Tkinter**: Biblioteca utilizada para la creación de la interfaz gráfica.
- **JSON**: Se usa para almacenar la información de usuarios y eventos.
- **Pillow (PIL)**: Para el manejo y redimensionado de imágenes en el dashboard de administrador.

## Requisitos previos
- **Python 3.11** o superior instalado en tu sistema (el script `install.py` verifica e instala Python 3.11 si es necesario).
- Clonar este repositorio en tu máquina local.

## Instalación

1. **Clona el repositorio en tu máquina local**:
   ```bash
   git clone https://github.com/SlotyHolly/Sistema-de-Gestion-de-Eventos
   cd Sistema-de-Gestion-de-Eventos
    ```
2. **Ejecuta el script de instalación `install.py`**:
- Este script verifica si tienes Python 3.11 instalado.
- Si Python 3.11 no está instalado, el script te guiará para instalarlo manualmente.
- Luego, el script crea un entorno virtual y se encarga de instalar las dependencias necesarias.

    **Para ejecutar el Script:**

    ```bash
    python install.py
    ```

    **El script se encargará de:**
    - Verificar que Python 3.11 esté instalado.
    - Crear un entorno virtual llamado `env`.
    - Instalar las dependencias desde el archivo `requirements.txt`.

3. **Ejecuta el proyecto: Después de instalar las dependencias, puedes ejecutar la aplicación con:**

    ```bash
    python src/main.py
    ```
## Estructura del proyecto

El proyecto sigue la siguiente estructura de carpetas:

```bash
Sistema-de-Gestion-de-Eventos/
│
├── src/
│   ├── main.py                    # Archivo principal que ejecuta la aplicación
│   ├── ui/                        # Carpeta que contiene las interfaces gráficas
│   │   ├── login.py               # Interfaz gráfica para el inicio de sesión
│   │   ├── register.py            # Interfaz gráfica para el registro de usuarios
│   │   ├── admin_dashboard.py     # Dashboard para los administradores
│   │   ├── user_dashboard.py      # Dashboard para los usuarios
│   │   ├── change_password.py     # Dashboard para gestionar el cambio de contrasena
│   │   └── recovery_password.py   # Interfaz gráfica para recuperar contraseñas
│   │
│   ├── functions/                 # Funciones principales para manejar la lógica del sistema
│   │   ├── login.py               # Función para validar credenciales de usuario
│   │   ├── registro.py            # Función para registrar nuevos usuarios
│   │   ├── events.py              # Función para el manejo de los eventos
│   │   └── password.py            # Función para la recuperación de contraseñas
│   │
│   └── data/                      # Carpeta que contiene la base de datos en formato JSON
│       ├── events_data/           # Carpeta que contiene los Flyers de los eventos
│       │   └── default_flyer.png  # Flyer Base
│       ├── users.json             # Archivo JSON que almacena la información de usuarios
│       └── events.json            # Archivo JSON que almacena la información de eventos
│
├── install.py                     # Script de instalación para verificar Python, crear entorno virtual e instalar dependencias
├── requirements.txt               # Archivo con las dependencias del proyecto
└── README.md                      # Este archivo
```

## Funcionalidades

1. **Login de usuario**

- Los usuarios pueden iniciar sesión con su nombre de usuario y contraseña.
- Los administradores también inician sesión desde la misma ventana.

2. **Registro de Usuario:**

- Los nuevos usuarios pueden registrarse proporcionando un nombre de usuario y una contraseña.
- Los usuarios por defecto reciben el rol de "usuario".

3. **Dashboard del Administrador:**

- Los administradores pueden cargar nuevos eventos, modificar los existentes, y cargar flyers para los eventos.

4. **Dashboard del Usuario:**

- Los usuarios pueden ver los eventos disponibles y comprar tickets. También tienen acceso a la lista de tickets adquiridos.

5. **Recuperación de Contraseña:**

- Si un usuario olvida su contraseña, puede usar la opción de "Recuperar Contraseña" e ingresar su nombre de usuario, el código de recuperación (por defecto es "1234") y la nueva contraseña.

## Requisitos Adicionales

Asegúrate de tener un archivo requirements.txt en la raíz del proyecto con las siguientes dependencias:

```bash
pillow==10.4.0
```
El archivo requirements.txt contiene todas las dependencias del proyecto y el script install.py se encargará de instalarlas automáticamente en el entorno virtual.

---

## Próximos pasos

- Mejoras de la UI: Hacer la interfaz más intuitiva y agregar más funcionalidades en el dashboard.
- Sistema de tickets avanzado: Implementar la funcionalidad de compra de tickets con inventarios de asientos y opciones de pago.
- Encriptación de contraseñas: Implementar encriptación de contraseñas usando hashlib o una biblioteca especializada como bcrypt para aumentar la seguridad.
- Logs de auditoría: Registrar las acciones importantes realizadas por los usuarios y administradores.

---

## Licencia
Este proyecto está bajo la licencia MIT.

---

## Notas
Este `README.md` incluye las instrucciones necesarias para clonar, instalar y ejecutar el proyecto utilizando el nuevo script `install.py`, que verifica la presencia de Python 3.11, crea un entorno virtual e instala las dependencias necesarias. Además, se incluyen instrucciones claras para el uso y desarrollo del proyecto.