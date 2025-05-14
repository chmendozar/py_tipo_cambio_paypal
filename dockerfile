# Archivo: Dockerfile
FROM python:3.13.3-slim

# Establecer variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# Instalar Chrome y dependencias necesarias
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    google-chrome-stable \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Crear directorio de logs y asegurar permisos
RUN mkdir -p /app/logs && chmod 777 /app/logs

# Copiar requerimientos y archivo Python
COPY . .

# Instalar dependencias
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Verificar la instalación
RUN python -c "import sys; print(f'Python {sys.version}')" && \
    python -c "import selenium; print(f'Selenium {selenium.__version__}')"

CMD ["python", "main.py"]