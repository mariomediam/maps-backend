# Usamos una imagen oficial de Python
FROM python:3.13.2

# Evitar que Python genere archivos .pyc y asegurar salida sin buffering
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Definir el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar requirements.txt e instalar dependencias
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar todo el código fuente al contenedor
COPY . /app/

# Instalar herramientas básicas útiles (opcional para producción)
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Cambiar al directorio de Django donde está manage.py
WORKDIR /app/maps

# Exponer el puerto 8000 para Django
EXPOSE 8000

# Configurar variables de entorno para producción
ENV DJANGO_SETTINGS_MODULE=maps.settings
ENV PYTHONPATH=/app/maps

# Ejecutar migraciones y colectar archivos estáticos, luego iniciar el servidor
CMD python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput && \
    python manage.py runserver 0.0.0.0:8000