from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# A tuple of 2-tuples added above our models
CARE_TIMES = (
    ('M', 'Morning'),
    ('A', 'Afternoon'),
    ('E', 'Evening')
)
#^the value that will be stored in the database,  the human-friendly “display” value

class Supply(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=20)
    color = models.CharField(max_length=20, blank=True, null=True)
    # blank=True: Allows the field to be left blank in forms (Django admin, etc.).
    # null=True: Allows the database to store NULL for this field.

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('supply-detail', kwargs={'pk': self.id})

# Create your models here.
class Plant(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    # Many-to-Many relationship with supplies
    supplies = models.ManyToManyField(Supply)
    # Add the foreign key linking to a user instance
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #^if plant get deleted its associated user get delete too
    
    def __str__(self):
        return self.name
    
    # Define a method to get the URL for this particular plant instance
    def get_absolute_url(self):
        # Use the 'reverse' function to dynamically find the URL for viewing this plant's details
        return reverse('plant-detail', kwargs={'plant_id': self.id})
    
class Care(models.Model):
    date = models.DateField('Care date')
    time_of_day = models.CharField(
        max_length=1,
        choices=CARE_TIMES,
        default=CARE_TIMES[0][0] #M for morning
    )

    # Connect each care entry to a plant
    # Create a plant_id column for each care in the database
    #care belongs to a Plant
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    #^one-ton-many relationship, if a Plant record is deleted, all the child Care will be deleted
    def __str__(self):
        return f"{self.get_time_of_day_display()} on {self.date}"
    
    class Meta:
        ordering = ['-date']  # This line makes the newest cares appear first