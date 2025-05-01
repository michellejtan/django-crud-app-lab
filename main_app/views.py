from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Plant, Supply
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
    supplies = Supply.objects.all() #fetch all supplies
    care_form = CareForm()
    return render(request, 'plants/detail.html', {
        'plant': plant, 'care_form': care_form,
        'supplies': supplies # pass suppliesto the template
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

def add_care(request, plant_id):
    # create a ModelForm instance using the data in request.POST
    form = CareForm(request.POST)
    # validate the form
    if form.is_valid():
        # don't save the form to the db until it
        # has the plant_id assigned
        new_feeding = form.save(commit=False)
        new_feeding.plant_id = plant_id
        new_feeding.save()
    return redirect('plant-detail', plant_id = plant_id)

class SupplyCreate(CreateView):
    model = Supply
    fields = '__all__'

class SupplyList(ListView):
    model = Supply

class SupplyDetail(DetailView):
    model = Supply

class SupplyUpdate(UpdateView):
    model = Supply
    fields = '__all__'
    # ['name', 'type', 'color']

class SupplyDelete(DeleteView):
    model = Supply
    success_url = '/supplies/'
