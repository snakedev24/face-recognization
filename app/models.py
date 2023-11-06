from django.db import models
from django.contrib.auth.models import User 
# Create your models here.



class ImageModel(models.Model):
    image = models.ImageField(upload_to='my_images/')
    name_of_employee = models.CharField(max_length=255)
    datetime_field = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name_of_employee