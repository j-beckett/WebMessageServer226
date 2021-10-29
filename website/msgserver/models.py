from django.db import models

class Message(models.Model):
    message = models.CharField(max_length=160)
    key = models.CharField(max_length=8)

    def __str__(self):
        return str(self.message) + ',' + str(self.key) 

# Create your models here.
