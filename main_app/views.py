from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from .models import Plant, Supply
from .forms import CareForm

# Create your views here.
# Import HttpResponse to send text-based responses
# from django.http import HttpResponse

# Define the home view function
# def home(request):
#     # Send a simple HTML response
#     # return HttpResponse('<h1>Hello ᓚᘏᗢ</h1>')
#     return render(request, 'home.html')
class Home(LoginView):
    template_name = 'home.html'

def plant_index(request):
    plants = Plant.objects.all()
    return render(request, 'plants/index.html', {
        'plants': plants
    })

def plant_detail(request, plant_id):
    plant = Plant.objects.get(id=plant_id)
    # supplies = Supply.objects.all() #fetch all supplies
    # Only get the supply the plant does not have
    supplies_plant_doesnt_have = Supply.objects.exclude(id__in = plant.supplies.all().values_list('id'))
    care_form = CareForm()
    return render(request, 'plants/detail.html', {
        'plant': plant, 'care_form': care_form,
        'supplies': supplies_plant_doesnt_have
        # 'supplies': supplies # pass suppliesto the template
    })
def remove_supply(request, plant_id, supply_id):
    # Plant.objects.get(id=plant_id).supplies.remove(supply_id)
    # ^ this finds a particular plant and removes a record from the join
    # table with that plant's id and the id of the supply thus deleting the relationship/association
    # Look up the plant
    plant = Plant.objects.get(id=plant_id)
    # Look up the supply
    supply = Supply.objects.get(id=supply_id)
    # Remove the supply from the plant
    plant.supplies.remove(supply)
    return redirect('plant-detail', plant_id=plant_id)

class PlantCreate(CreateView):
    model = Plant
    # fields = '__all__'
    # more explicit
    fields = ['name', 'species', 'description', 'age']
    # success_url = '/plants/' #static page

    # This inherited method is called when a
    # valid plant form is being submitted
    def form_valid(self, form):
        # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user  # form.instance is the plant
        # Let the CreateView do its job as usual
        return super().form_valid(form)



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

def associate_supply(request, plant_id, supply_id):
    Plant.objects.get(id=plant_id).supplies.add(supply_id)
    return redirect('plant-detail', plant_id=plant_id)
