from django.db import models

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
