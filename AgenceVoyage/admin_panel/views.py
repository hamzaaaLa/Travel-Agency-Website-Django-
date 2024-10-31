from .models import Categorie,Country,Destination,Avion,Hotel,Voyage,Promotion,NotificationClient,NotificationAdmin,CompteVisa,ComptePayPal,Reservation
from users.models import Users
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.core.serializers import serialize
from django.contrib.auth import logout



def view(request):
    return render(request,'admin_panel/ajoutComptePaypal.html')

def ajoutVisa(request):
    ComptePayPal.objects.create(
        nomComplet="Ali El",
        cardNumber="3333-3333-3333",
        code="12345",
        solde=5000.00
    )
    referer = request.META.get('HTTP_REFERER')
    return redirect(referer)


def get_avions_and_hotels(request):
    if request.method == 'GET' and 'destination_id' in request.GET:
        destination_id = request.GET.get('destination_id')
        avions = Avion.objects.filter(destination_id=destination_id).values_list('id', 'nomAvion')
        hotels = Hotel.objects.filter(localisation_id=destination_id).values_list('id', 'hotelNom')
        avions_dict = dict(avions)
        hotels_dict = dict(hotels)
        return JsonResponse({'avions': avions_dict, 'hotels': hotels_dict})
    else:
        return JsonResponse({'error': 'Invalid request'})
def get_avion_and_hotel_by_destination(request):
    selected_destination_id = request.GET.get('destination_id')

    if selected_destination_id:
        # Fetch avions for the selected destination
        avions = Avion.objects.filter(destination_id=selected_destination_id)

        # Fetch hotels for the selected destination
        hotels = Hotel.objects.filter(localisation_id=selected_destination_id)

        # Create JSON response with avion and hotel options
        data = {
            'avion_options': [{'id': avion.id, 'nomAvion': avion.nomAvion} for avion in avions],
            'hotel_options': [{'id': hotel.id, 'hotelNom': hotel.hotelNom} for hotel in hotels]
        }
    else:
        data = {'avion_options': [], 'hotel_options': []}

    return JsonResponse(data)

def get_countries_by_category(request):
    if request.method == 'GET' and request.is_ajax():
        category_id = request.GET.get('category')

        if category_id:
            # Ensure the category exists
            category = get_object_or_404(Categorie, id=category_id)

            # Fetch countries based on the selected category
            countries = Country.objects.filter(categorie=category).values('id', 'nom')

            return JsonResponse(list(countries), safe=False)

    return JsonResponse({'error': 'Invalid request'})

def get_destinations_by_country(request):
    if request.method == 'GET' and request.is_ajax():
        country_id = request.GET.get('country')

        # Fetch destinations based on the selected country
        destinations = Destination.objects.filter(country_id=country_id).values('id', 'nom')

        return JsonResponse(list(destinations), safe=False)

    return JsonResponse({'error': 'Invalid request'})

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
    notifications=NotificationAdmin.objects.all()
    categ=Categorie.objects.all()
    avions=Avion.objects.all()
    dest=Destination.objects.all()
    voyages=Voyage.objects.all()
    hotels=Hotel.objects.all()
    return render(request,'admin_panel/gestionVoyage.html',{'notifications':notifications,'voyages':voyages,'hotels':hotels,'avions':avions,'categ': categ, 'dest':dest})
def gestionAvion(request):
    notifications=NotificationAdmin.objects.all()
    dest=Destination.objects.all()
    avions=Avion.objects.all()
    return render(request,'admin_panel/gestionAvion.html',{'notifications':notifications,'avions':avions,'dest':dest})
def gestionHotel(request):
    notifications=NotificationAdmin.objects.all()
    dest=Destination.objects.all()
    hotels=Hotel.objects.all()
    return render(request,'admin_panel/gestionHotel.html',{'notifications':notifications,'hotels':hotels,'dest':dest})

def gestionCategorie(request):
    notifications=NotificationAdmin.objects.all()
    data = Categorie.objects.all()
    return render(request,'admin_panel/gestionCategorie.html',{'notifications':notifications,'data': data})

def gestionCountrie(request):
    notifications=NotificationAdmin.objects.all()
    categ = Categorie.objects.all()
    countries=Country.objects.all()
    return render(request,'admin_panel/gestionCountrie.html',{'notifications':notifications,'categ': categ, 'countries': countries})


def editDestinationForm(request,pk):
    destination = get_object_or_404(Destination, id=pk)
    return render(request,'admin_panel/modifierDestination.html',{'dest':destination})



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
def deleteDes(request, pk):
    des=get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        des.delete()
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)

#--------------------gestion des categories--------------------
def editCategorie(request, pk):
    categorie = get_object_or_404(Categorie,pk=pk)

    if request.method == 'POST':
        # Update the instance with the submitted data
        categorie.nom = request.POST.get('nomCategorie')
        categorie.photo = request.FILES.get('photo')
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
    notifications=NotificationAdmin.objects.all()
    categ=Categorie.objects.all()
    countries=Country.objects.all()
    dest=Destination.objects.all()
    return render(request,'admin_panel/gestionVille.html',{'notifications':notifications,'categ': categ, 'countries': countries,'dest':dest})
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


def ajoutVoyage(request):
    if request.method == 'POST':
        destination_id = request.POST.get('destination')
        avion_id = request.POST.get('avion')
        hotel_id = request.POST.get('hotel')
        duration = request.POST.get('duration')
        price = request.POST.get('price')
        description = request.POST.get('description')
        photo = request.FILES.get('photo')
        nombre_places = request.POST.get('nombre_places')  # Retrieve number of places

        try:
            destination = Destination.objects.get(id=destination_id)
            avion = Avion.objects.get(id=avion_id)
            hotel = Hotel.objects.get(id=hotel_id)
        except (Destination.DoesNotExist, Avion.DoesNotExist, Hotel.DoesNotExist):
            raise Http404("Destination, Avion, or Hotel does not exist")

        NotificationClient.objects.create(
            description="New trip is added",
            voyage=destination.nom
        )

        Voyage.objects.create(
            destination=destination,
            avion=avion,
            hotel=hotel,
            duration=duration,
            prix=price,
            description=description,
            photo=photo,
            nombre_places=nombre_places  # Save number of places
        )

        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)  # Redirect back to the previous page

def editDestination(request):
    print('hello')

def logout_view(request):

    logout(request)
    return redirect('trips:home') 

def editVoyage(request, pk):
    voyage = get_object_or_404(Voyage, pk=pk)

    if request.method == 'POST':
        destination_id = request.POST.get('destination')
        avion_id = request.POST.get('avion')
        hotel_id = request.POST.get('hotel')
        destination=get_object_or_404(Destination, id=destination_id)
        
        try:
            destination = Destination.objects.get(id=destination_id)
            avion = Avion.objects.get(id=avion_id)
            hotel = Hotel.objects.get(id=hotel_id)
        except (Destination.DoesNotExist, Avion.DoesNotExist, Hotel.DoesNotExist):
            raise Http404("Destination, Avion, or Hotel does not exist")
        # Update the instance with the submitted data
        voyage.duration = request.POST.get('duration')
        voyage.prix = request.POST.get('prix')
        voyage.description = request.POST.get('description')
        voyage.nombre_places = request.POST.get('nombre_places')
        voyage.destination = destination
        voyage.avion = avion
        voyage.hotel = hotel
        voyage.photo = request.FILES.get('photo')
        voyage.save()
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)  # Replace with the actual view name or URL
    else:
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)  # Replace with your template name

def deleteVoyage(request, pk):
    voyage = get_object_or_404(Voyage, pk=pk)
    if request.method == 'POST':
        voyage.delete()
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)   


def ajoutAvion(request):
    if request.method == 'POST':
        destination_id = request.POST.get('destination')
        nomAvion = request.POST.get('nomAvion')
        Departure = request.POST.get('Departure')
        Departure_date = request.POST.get('Departure_date')
        Return_date = request.POST.get('Return_date')
        price = request.POST.get('price')
          # Retrieve number of places

        try:
            destination = Destination.objects.get(id=destination_id)
        except (Destination.DoesNotExist, Avion.DoesNotExist, Hotel.DoesNotExist):
            raise Http404("Destination, Avion, or Hotel does not exist")

        Avion.objects.create(
            destination=destination,
            nomAvion=nomAvion,
            villeDepart=Departure,
            dateDepart=Departure_date,
            dateRetour=Return_date,
            prix=price,
 # Save number of places
        )

        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)  # Redirect back to the previous page


def editAvion(request, pk):
    avion = get_object_or_404(Avion, pk=pk)

    if request.method == 'POST':
        destination_id = request.POST.get('destination')
        destination=get_object_or_404(Destination, id=destination_id)
        try:
            destination = Destination.objects.get(id=destination_id)
        except (Destination.DoesNotExist):
            raise Http404("Destination, Avion, or Hotel does not exist")
        # Update the instance with the submitted data
        avion.destination = destination
        avion.nomAvion = request.POST.get('nomAvion')
        avion.villeDepart = request.POST.get('Departure')
        avion.dateDepart = request.POST.get('Departure_date')
        avion.dateRetour = request.POST.get('Return_date')
        avion.prix = request.POST.get('prix')
        avion.save()
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)  # Replace with the actual view name or URL
    else:
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)  # Replace with your template name

def deleteAvion(request, pk):
    avion = get_object_or_404(Avion, pk=pk)
    if request.method == 'POST':
        avion.delete()
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)   
    

def ajoutHotel(request):
    if request.method == 'POST':
        destination_id = request.POST.get('destination')
        hotelNom = request.POST.get('hotelNom')
        etoile = request.POST.get('etoile')
        prixChambreSingle = request.POST.get('prixChambreSingle')
        prixChambreDouble = request.POST.get('prixChambreDouble') 
        prixChambreSubTriple = request.POST.get('prixChambreSubTriple')
        prixEnfant = request.POST.get('prixEnfant') 
        prixBebe = request.POST.get('prixBebe')

        try:
            destination = Destination.objects.get(id=destination_id)
        except (Destination.DoesNotExist, Avion.DoesNotExist, Hotel.DoesNotExist):
            raise Http404("Destination, Avion, or Hotel does not exist")

        Hotel.objects.create(
            localisation=destination,
            hotelNom=hotelNom,
            etoile=etoile,
            prixChambreSingle=prixChambreSingle,
            prixChambreDouble=prixChambreDouble,
            prixChambreSubTriple=prixChambreSubTriple,
            prixEnfant=prixEnfant,
            prixBebe=prixBebe  # Save number of places
        )

        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)  # Redirect back to the previous page


def editHotel(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)

    if request.method == 'POST':
        destination_id = request.POST.get('destination')
        destination=get_object_or_404(Destination, id=destination_id)
        
        try:
            destination = Destination.objects.get(id=destination_id)
        except (Destination.DoesNotExist):
            raise Http404("Destination doesn't exist")
        # Update the instance with the submitted data
        hotel.hotelNom = request.POST.get('hotelNom')
        hotel.etoile = request.POST.get('etoile')
        hotel.prixChambreSingle = request.POST.get('prixChambreSingle')
        hotel.prixChambreDouble = request.POST.get('prixChambreDouble')
        hotel.prixChambreSubTriple = request.POST.get('prixChambreSubTriple')
        hotel.prixEnfant = request.POST.get('prixEnfant')
        hotel.prixBebe = request.POST.get('prixBebe')
        hotel.localisation = destination
        hotel.save()
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)  # Replace with the actual view name or URL
    else:
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)  # Replace with your template name

def deleteHotel(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    if request.method == 'POST':
        hotel.delete()
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)   



def gestionClient(request):
    notifications=NotificationAdmin.objects.all()
    clients = Users.objects.all()
    return render(request,'admin_panel/gestionClient.html',{'notifications':notifications,'clients': clients})
def ajoutClient(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password=request.POST.get('password')
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        phone = request.POST.get('phone') 
        photo = request.FILES.get('photo')
        Users.objects.create(
            username=username,
            password=password,
            last_name=last_name,
            first_name=first_name,
            phone=phone,
            photo=photo,
        )

        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)  # Redirect back to the previous page


def editClient(request, pk):
    Client = get_object_or_404(Users, pk=pk)

    if request.method == 'POST':
    
        # Update the instance with the submitted data
        Client.username = request.POST.get('username')
        Client.last_name = request.POST.get('last_name')
        Client.first_name = request.POST.get('first_name')
        Client.phone = request.POST.get('phone') 
        Client.photo = request.FILES.get('photo')
        Client.save()
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)  # Replace with the actual view name or URL
    else:
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)  # Replace with your template name

def deleteClient(request, pk):
    Client = get_object_or_404(Users, pk=pk)
    if request.method == 'POST':
        Client.delete()
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)   

def addPromotion(request):
    if request.method == 'POST':
        id_voyage = request.POST.get('voyage')
        voyage = get_object_or_404(Voyage, pk=id_voyage)
        pourcentage = request.POST.get('pourcentage')
        newPrice = request.POST.get('newPrice')
        dateDebut = request.POST.get('dateDebut') 
        dateFin = request.POST.get('dateFin')
        voyage.prix=newPrice
        voyage.save()
        Promotion.objects.create(
            voyage=voyage,
            pourcentagePromotion=pourcentage,
            nouveauPrix=newPrice,
            dateDebut=dateDebut,
            dateFin=dateFin,
        )

        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)  # Redirect back to the previous page
    
def gestionPromotion(request):
    notifications=NotificationAdmin.objects.all()
    promotions = Promotion.objects.all()
    return render(request,'admin_panel/gestionPromotion.html',{'notifications':notifications,'promotions': promotions})

def deletePromotion(request, pk):
    promotion = get_object_or_404(Promotion, pk=pk)
    voyage=promotion.voyage
    price=promotion.nouveauPrix
    percentage=promotion.pourcentagePromotion
    voyage.prix=price/(1-(percentage/100))
    voyage.save()
    if request.method == 'POST':
        voyage.prix=price/(1-(percentage/100))
        voyage.save()
        promotion.delete()
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)  
    
def profile(request):
    notifications=NotificationAdmin.objects.all()
    user = request.user
    return render(request,'admin_panel/profile.html',{'notifications':notifications,'user':user})

def editProfileView(request):
    notifications=NotificationAdmin.objects.all()
    user = request.user
    return render(request,'admin_panel/editProfile.html',{'notifications':notifications,'user':user})

def saveProfileChange(request):
    user = request.user

    if request.method == 'POST':
        # Update the instance with the submitted data
        user.first_name = request.POST.get('firstName')
        user.last_name = request.POST.get('lastName')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.adresse = request.POST.get('adresse')
        user.photo = request.FILES.get('photo')
        user.save()
        referer = request.META.get('HTTP_REFERER')
        return redirect('profileAdmin')  # Replace with the actual view name or URL
    else:
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)  # Replace with your template name
    

def GReservation(request):
    notifications=NotificationAdmin.objects.all()
    reservs=Reservation.objects.all()
    return render(request,'admin_panel/Reservation.html',{'notifications':notifications,'reservs': reservs})
