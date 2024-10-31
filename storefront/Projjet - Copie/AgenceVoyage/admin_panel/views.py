from .models import Voyage,Categorie,Country,Destination
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.core.serializers import serialize


def get_countries_by_category(request):
    if request.method == 'GET' and request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        category_id = request.GET.get('category')

        if category_id:
            try:
                # Ensure the category exists
                category = Categorie.objects.get(id=category_id)

                # Fetch countries based on the selected category
                countries = Country.objects.filter(categorie=category).values('id', 'nom')

                return JsonResponse({'countries': list(countries)})
            except Categorie.DoesNotExist:
                return JsonResponse({'error': 'Category not found'}, status=404)

        return JsonResponse({'error': 'Invalid request'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


def get_destinations_by_country(request):
    selected_country_id = request.GET.get('country_id')
    
    if selected_country_id:
        # Fetch destinations for the selected country
        destinations = Destination.objects.filter(country_id=selected_country_id)
        data = {'destinations': [{'id': destination.id, 'nom': destination.nom} for destination in destinations]}
    else:
        data = {'destinations': []}

    return JsonResponse(data)

def get_countriesDestination(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'GET':
        category_id = request.GET.get('category_id')
        if category_id:
            # Assuming you have a ForeignKey from Country to Categorie
            countries = Country.objects.filter(categorie__id=category_id)

            # Create a list of dictionaries for the JSON response
            country_list = [{'id': country.id, 'nom': country.nom} for country in countries]

            # Return the list as JSON
            return JsonResponse({'countries': country_list})

    # If something goes wrong or the request is not AJAX, return an empty response
    return JsonResponse({})

def get_countries(request):
    selected_category_id = request.GET.get('category_id')
    
    if selected_category_id:
        # Fetch countries for the selected category
        countries = Country.objects.filter(categorie_id=selected_category_id)
        data = {'countries': [{'id': country.id, 'nom': country.nom} for country in countries]}
    else:
        data = {'countries': []}

    return JsonResponse(data)




def home(request):
    return render(request,'admin_panel/base.html')

def gestionVoyage(request):
    categ=Categorie.objects.all()
    countries=Country.objects.all()
    dest=Destination.objects.all()
    voyage=Voyage.objects.all()
    return render(request,'admin_panel/gestionVoyage.html',{'categ': categ,'voyages':voyage, 'countries': countries,'dest':dest})

def gestionCategorie(request):
    data = Categorie.objects.all()
    return render(request,'admin_panel/gestionCategorie.html',{'data': data})

def gestionCountrie(request):
    categ = Categorie.objects.all()
    countries=Country.objects.all()
    return render(request,'admin_panel/gestionCountrie.html',{'categ': categ, 'countries': countries})


def editDestination(request,pk):
    destination = get_object_or_404(Destination,pk=pk)

    if request.method == 'POST':

        idCountry=request.POST.get('country')
        country=get_object_or_404(Country, id=idCountry)
        # Update the instance with the submitted data
        destination.nom = request.POST.get('nomDestination')
        destination.country = country
        destination.photo = request.FILES.get('photo')
        destination.save()
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)  # Replace with the actual view name or URL
    else:
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)  # Replace with your template name

def ajoutVoyage(request):
    if request.method=='POST':
        duration=request.POST.get('duration')
        price=request.POST.get('price')
        description=request.POST.get('description')
        photo=request.FILES.get('photo')
        destinationId=request.POST.get('destination')
        try:
            # Get the category with the given id
            destination =Destination.objects.get(id=destinationId)
        except Categorie.DoesNotExist:
            raise Http404("Destination does not exist")
        Voyage.objects.create(
            destination=destination,
            duration=duration,
            price=price,
            description=description,
            photo=photo
        )
        return render(request, 'admin_panel/gestionVoyage.html')  # Replace with the actual view name or URL
    else:
        return render(request, 'admin_panel/gestionVoyage.html')  # Replace with your template name

def ajoutCategorie(request):
    if request.method=='POST':
        nomCategorie=request.POST.get('nomCategorie')
        photo=request.FILES.get('photo')

        Categorie.objects.create(
            nom=nomCategorie,
            photo=photo
        )
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)  # Replace with the actual view name or URL
    else:
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)  # Replace with your template name


def ajoutCountry(request):
    if request.method=='POST':
        nomCountry=request.POST.get('nomCountry')
        categorieId=request.POST.get('categorie')
        photo=request.FILES.get('photo')

        try:
            # Get the category with the given id
            categorie = Categorie.objects.get(id=categorieId)
        except Categorie.DoesNotExist:
            raise Http404("Category does not exist")

        Country.objects.create(
            nom=nomCountry,
            categorie=categorie,
            photo=photo
        )
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)  # Replace with the actual view name or URL

def editCountry(request, pk):
    country = get_object_or_404(Country,pk=pk)

    if request.method == 'POST':
        idCateg=request.POST.get('categorie')
        categorie=get_object_or_404(Categorie, id=idCateg)

        # Update the instance with the submitted data
        country.nom = request.POST.get('nomCountry')
        country.categorie = categorie
        country.photo = request.FILES.get('photo')
        country.save()
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)  # Replace with the actual view name or URL
    else:
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)  # Replace with your template name

def deleteCountry(request, pk):
    country=get_object_or_404(Country, pk=pk)
    if request.method == 'POST':
        country.delete()
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)   # Redirect to a suitable URL after deletion

#--------------------gestion des categories--------------------
def editCategorie(request, pk):
    categorie = get_object_or_404(Categorie,pk=pk)

    if request.method == 'POST':
        # Update the instance with the submitted data
        categorie.nom = request.POST.get('nomCategorie')
        categorie.photo = request.POST.get('photo')
        categorie.save()
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)  # Replace with the actual view name or URL
    else:
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)  # Replace with your template name

def deleteCategorie(request, pk):
    categ=get_object_or_404(Categorie, pk=pk)

    if request.method == 'POST':
        categ.delete()
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)   # Redirect to a suitable URL after deletion
    

def gestionVille(request):
    categ=Categorie.objects.all()
    countries=Country.objects.all()
    dest=Destination.objects.all()
    return render(request,'admin_panel/gestionVille.html',{'categ': categ, 'countries': countries,'dest':dest})
# Create your views here.
def ajoutDestination(request):
    if request.method=='POST':
        nomDestination=request.POST.get('nomDestination')
        countryId=request.POST.get('country')
        photo=request.FILES.get('photo')

        try:
            # Get the category with the given id
            country = Country.objects.get(id=countryId)
        except Country.DoesNotExist:
            raise Http404("Country does not exist")

        Destination.objects.create(
            nom=nomDestination,
            country=country,
            photo=photo
        )
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)  # Replace with the actual view name or URL

def deleteDestination(request, pk):
    destination=get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        destination.delete()
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer) 

