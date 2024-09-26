import os
import subprocess
import sys
import venv
import platform

# URL para descargar Python 3.11 en Windows
PYTHON_DOWNLOAD_URL_WIN = "https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe"
PYTHON_DOWNLOAD_URL_MAC = "https://www.python.org/ftp/python/3.11.9/python-3.11.9-macos11.pkg"
PYTHON_DOWNLOAD_URL_LINUX = "https://www.python.org/downloads/source/"

def is_python_3_11_installed():
    """Verifica si Python 3.11 está instalado en el sistema."""
    try:
        output = subprocess.check_output(["python3.11", "--version"], universal_newlines=True)
        if "3.11.9" in output:
            return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    try:
        output = subprocess.check_output(["python", "--version"], universal_newlines=True)
        if "3.11.9" in output:
            return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

    return False

def install_python_3_11():
    """Guía para instalar Python 3.11 según el sistema operativo."""
    os_type = platform.system()

    if os_type == "Windows":
        print("Python 3.11 no está instalado. Descargando e instalando para Windows...")
        os.system(f"start {PYTHON_DOWNLOAD_URL_WIN}")
        print("Descargue e instale Python 3.11 manualmente, luego ejecute este script nuevamente.")
    elif os_type == "Darwin":  # MacOS
        print("Python 3.11 no está instalado. Descargando e instalando para macOS...")
        os.system(f"open {PYTHON_DOWNLOAD_URL_MAC}")
        print("Descargue e instale Python 3.11 manualmente, luego ejecute este script nuevamente.")
    elif os_type == "Linux":
        print("Python 3.11 no está instalado. Abriendo la página de descargas para Linux...")
        print("Use su administrador de paquetes (apt, yum, dnf, etc.) para instalar Python 3.11, o descárguelo desde:")
        os.system(f"xdg-open {PYTHON_DOWNLOAD_URL_LINUX}")
    else:
        print(f"Sistema operativo no soportado: {os_type}. Instale Python 3.11 manualmente.")
    
    sys.exit(1)

def create_virtual_environment():
    """Crea un entorno virtual llamado 'env'."""
    print("Creando un entorno virtual...")
    venv_dir = os.path.join(os.getcwd(), "env")
    venv.create(venv_dir, with_pip=True)
    print("Entorno virtual creado en 'env/'.")

def install_requirements():
    """Instala las dependencias desde requirements.txt."""
    print("Instalando dependencias desde requirements.txt...")
    venv_python = os.path.join(os.getcwd(), "env", "Scripts", "python") if platform.system() == "Windows" else os.path.join(os.getcwd(), "env", "bin", "python")
    subprocess.check_call([venv_python, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([venv_python, "-m", "pip", "install", "-r", "requirements.txt"])
    print("Dependencias instaladas.")

def main():
    # Verificar si Python 3.11 está instalado
    if not is_python_3_11_installed():
        install_python_3_11()

    # Crear entorno virtual
    create_virtual_environment()

    # Instalar dependencias
    install_requirements()

    print("Instalación completa. Ahora puede ejecutar 'main.py' dentro del entorno virtual.")

if __name__ == "__main__":
    main()
