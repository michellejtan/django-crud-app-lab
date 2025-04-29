from django.contrib import admin
from .models import Plant, Care
# Register your models here.
admin.site.register([Plant, Care])