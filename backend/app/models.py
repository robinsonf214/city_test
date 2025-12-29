from django.db import models


class City(models.Model):
    name = models.CharField(max_length=120)
    country = models.CharField(max_length=120)
    latitude = models.FloatField()
    longitude = models.FloatField()
    main_tourist_site = models.TextField()
    population = models.PositiveIntegerField()
    has_seaport = models.BooleanField(default=False)

    temperature = models.FloatField(null=True, blank=True) 
    is_active = models.BooleanField(default=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["is_active"]),
            models.Index(fields=["country", "name"]),
        ]



class WeatherRequestLog(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="weather_logs")
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField(null=True, blank=True)
    status_code = models.PositiveSmallIntegerField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-started_at"]
        indexes = [
            models.Index(fields=["city", "started_at"]),
        ]

    