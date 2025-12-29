# City Service – Backend (Django + DRF + Celery)

Backend desarrollado en Django Rest Framework que gestiona ciudades y actualiza automáticamente su temperatura cada 5 minutos usando Celery + Redis y la API pública de Open-Meteo.

## 📌 Stack Tecnológico

- Python 3.12
- Django 4.2
- Django REST Framework
- PostgreSQL
- Redis
- Celery + Celery Beat
- Open-Meteo API (pública)

## 1️⃣ Requisitos

- Docker
- Docker Compose
- Python 3.12+

## 2️⃣ Clonar el repositorio

bash
git clone <repo_url>
cd city_service


## 3️⃣ Variables de entorno (host)
Crear el archivo .env | .env.local
Para la práctica se envía .env.local dentro del repositorio.

## 4️⃣ Levantar infraestructura (Postgres + Redis + Celery)
$docker-compose -f docker-compose.infra.yml up -d --build

Verificar:
$docker-compose -f docker-compose.infra.yml ps

Debe mostrar algo similar:

Name,Command,State,Ports
city_service_beat_1,celery -A city_service bea ...,Up,
city_service_celery_1,celery -A city_service wor ...,Up,
city_service_db_1,docker-entrypoint.sh postgres,Up,"0.0.0.0:5432->5432/tcp,:::5432->5432/tcp"
city_service_redis_1,docker-entrypoint.sh redis ...,Up,"0.0.0.0:6379->6379/tcp,:::6379->6379/tcp"

## 5️⃣ Backend Django (host con venv)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Migraciones:
cd backend
set -a; source ../.env.local; set +a
python manage.py makemigrations 
python manage.py migrate

Levantar servicio:
python manage.py runserver 0.0.0.0:8000

## 📡 Endpoints disponibles
Colección de endpoints en:
 - /endpoints/city_temp.postman_collection.json

 ## 🌡️ Actualización automática de temperatura

 Cada 5 minutos, Celery Beat ejecuta la tarea:
    app.tasks.update_city_temperatures
    Para cada ciudad activa:

    -Consulta la API de Open-Meteo usando latitud y longitud
    -Actualiza el campo temperature
    -Registra la ejecución en WeatherRequestLog

## 🧾 Registro de ejecuciones (WeatherRequestLog)

ada ejecución genera un log con:

-Ciudad
-Hora de inicio
-Hora de fin
-Código HTTP
-Mensaje de error (si existe)

Esto permite trazabilidad completa de las llamadas a la API externa.

## 👨‍💻 Autor
    Desarrollado por Robinson Flores
    Backend Developer – Django / DRF / Celery