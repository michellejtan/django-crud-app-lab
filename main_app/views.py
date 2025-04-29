from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Plant
from .forms import CareForm

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

def plant_detail(request, plant_id):
    plant = Plant.objects.get(id=plant_id)
    care_form = CareForm()
    return render(request, 'plants/detail.html', {
        'plant': plant, 'care_form': care_form
    })

class PlantCreate(CreateView):
    model = Plant
    # fields = '__all__'
    # more explicit
    fields = ['name', 'species', 'description', 'age']
    # success_url = '/plants/' #static page

class PlantUpdate(UpdateView):
    model = Plant
    # things could be misspell
    fields = ['name', 'species', 'description', 'age']

class PlantDelete(DeleteView):
    model = Plant
    success_url = '/plants/' #make sense in this case, it's no longer in database after delete


