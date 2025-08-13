## Inicia un contenedor vacio para que luego se pueda ingresar en el e instalar lo que se desee

'''
docker compose up --build
'''

### Construye la imagen:
'''
docker-compose build
'''

### Crea el proyecto dentro del contenedor:
'''
docker-compose run web django-admin startproject mi_proyecto .
'''

### Levanta el contenedor para ejecutar el proyecto:
'''
docker-compose up
'''