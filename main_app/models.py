from django.db import models
from django.urls import reverse

# Create your models here.
class Plant(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    # Many-to-Many relationship with supplies
    # supplies = models.ManyToManyField(Supply)

    def __str__(self):
        return self.name
    
    # Define a method to get the URL for this particular plant instance
    def get_absolute_url(self):
        # Use the 'reverse' function to dynamically find the URL for viewing this plant's details
        return reverse('plant-detail', kwargs={'plant_id': self.id})