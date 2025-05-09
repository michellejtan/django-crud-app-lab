from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from .models import Plant, Supply
from .forms import CareForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required # to protect view functions
# Import the mixin for class-based views
from django.contrib.auth.mixins import LoginRequiredMixin

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

def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        # form = UserCreationForm(request.POST)
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in
            login(request, user)
            return redirect('plant-index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    # form = UserCreationForm()
    form = CustomUserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)
    # Same as: 
    # return render(
    #     request, 
    #     'signup.html',
    #     {'form': form, 'error_message': error_message}
    # )

@login_required
def plant_index(request):
    # This reads ALL plants, not just the logged in user's plants
    # plants = Plant.objects.all()
    plants = Plant.objects.filter(user=request.user)
    # You could also retrieve the logged in user's plants like this
    # plants = request.user.plant_set.all()
    return render(request, 'plants/index.html', {
        'plants': plants
    })

@login_required
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

@login_required
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

class PlantCreate(LoginRequiredMixin, CreateView):
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



class PlantUpdate(LoginRequiredMixin, UpdateView):
    model = Plant
    # things could be misspell
    fields = ['name', 'species', 'description', 'age']

class PlantDelete(LoginRequiredMixin, DeleteView):
    model = Plant
    success_url = '/plants/' #make sense in this case, it's no longer in database after delete

@login_required
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

class SupplyCreate(LoginRequiredMixin, CreateView):
    model = Supply
    fields = '__all__'

class SupplyList(LoginRequiredMixin, ListView):
    model = Supply

class SupplyDetail(LoginRequiredMixin, DetailView):
    model = Supply

class SupplyUpdate(LoginRequiredMixin, UpdateView):
    model = Supply
    fields = '__all__'
    # ['name', 'type', 'color']

class SupplyDelete(LoginRequiredMixin, DeleteView):
    model = Supply
    success_url = '/supplies/'

@login_required
def associate_supply(request, plant_id, supply_id):
    Plant.objects.get(id=plant_id).supplies.add(supply_id)
    return redirect('plant-detail', plant_id=plant_id)