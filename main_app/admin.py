from django.contrib import admin
from .models import Plant, Care, Supply
# Register your models here.
admin.site.register([Plant, Care, Supply])