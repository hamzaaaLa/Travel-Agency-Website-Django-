from django.shortcuts import render
from admin_panel.models import Voyage
# Create your views here.
def home(request):
     Voyages= Voyage.objects.all()
     context={'Voyages':Voyages}
     return render(request,'trips/home.html',context)

def voyage(request, pk):
    voyage = Voyage.objects.filter(pk=pk).first()
    context = {'voyage': voyage}
    return render(request, 'trips/Voyage.html', context)
   
