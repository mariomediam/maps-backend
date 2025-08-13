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

# Instalar herramientas básicas útiles
RUN apt-get update && apt-get install -y \
    vim \
    nano \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Exponer el puerto 8000 para Django
EXPOSE 8000

# Crear script de inicio
RUN echo '#!/bin/bash\ncd /app\nif [ -f "maps/manage.py" ]; then\n    echo "Ejecutando Django desde /app/maps..."\n    cd maps\n    python manage.py runserver 0.0.0.0:8000\nelse\n    echo "No se encontró manage.py, manteniendo contenedor activo..."\n    tail -f /dev/null\nfi' > /start.sh && chmod +x /start.sh

# Ejecutar el script de inicio
CMD ["/start.sh"]