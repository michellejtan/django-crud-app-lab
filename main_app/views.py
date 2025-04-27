from django.shortcuts import render
from .models import Plant
# Create your views here.
# Import HttpResponse to send text-based responses
# from django.http import HttpResponse

# Define the home view function
def home(request):
    # Send a simple HTML response
    # return HttpResponse('<h1>Hello ᓚᘏᗢ</h1>')
    return render(request, 'home.html')


def plant_index(request):
    plants = Plant.objects.all()
    return render(request, 'plants/index.html', {
        'plants': plants
    })
