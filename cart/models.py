from django.db import models

class Session(models.Model):
    session_key = models.CharField(max_length=128)
    payment_id = models.CharField(max_length=128)
