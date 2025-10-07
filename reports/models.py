from django.db import models

class Fuite(models.Model):
    description = models.TextField()
    photo = models.ImageField(upload_to="fuites/")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    date_signalement = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        
        return f"Fuite du {self.date_signalement.strftime('%d/%m/%Y %H:M')}"
    