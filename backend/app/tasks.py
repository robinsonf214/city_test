from __future__ import annotations

import os
import requests
from celery import shared_task
from django.db import transaction
from django.utils import timezone

from .models import City, WeatherRequestLog

OPEN_METEO_URL = os.getenv("OPEN_METEO_URL", "https://api.open-meteo.com/v1/forecast")


def _build_params(city: City) -> dict:
    return {
        "latitude": city.latitude,
        "longitude": city.longitude,
        "current": "temperature_2m",
        "timezone": "auto",
    }


def _extract_temperature(payload: dict) -> float:
    current = payload.get("current") or {}
    temp = current.get("temperature_2m")
    if temp is None:
        raise ValueError("Respuesta sin current.temperature_2m")
    return float(temp)


@shared_task(name="app.tasks.update_city_temperatures")
def update_city_temperatures():
    cities = City.objects.filter(is_active=True)

    for city in cities:
        log = WeatherRequestLog.objects.create(
            city=city,
            started_at=timezone.now(),
        )

        try:
            resp = requests.get(OPEN_METEO_URL, params=_build_params(city), timeout=15)
            log.status_code = resp.status_code

            if 200 <= resp.status_code < 300:
                temp = _extract_temperature(resp.json())
                with transaction.atomic():
                    City.objects.filter(pk=city.pk).update(temperature=temp)
            else:
                log.error_message = f"HTTP {resp.status_code}: {resp.text[:300]}"

        except Exception as e:
            log.error_message = str(e)

        finally:
            log.finished_at = timezone.now()
            log.save(update_fields=["finished_at", "status_code", "error_message"])
