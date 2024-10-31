from django.shortcuts import render,redirect
from django.shortcuts import  get_object_or_404
from admin_panel.models import Country,Reservation,Promotion
from admin_panel.models import Voyage,CompteVisa
from admin_panel.models import Categorie
from django.db.models import Q
from django.http import JsonResponse
from admin_panel.models import ComptePayPal,NotificationClient,NotificationAdmin
from django.contrib import messages
from decimal import Decimal
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect

# Create your views here.
def home(request):
     
     Countries= Country.objects.all()
     Promos= Promotion.objects.all()
     context={'Countries':Countries,'Promos':Promos}
     return render(request,'trips/home.html',context)

def tripsv(request): 
    query = request.GET.get('query')
    sort_option = request.GET.get('sort_option')
    min_price = request.GET.get('min_price')
    min_duration = request.GET.get('min_duration')
    category_id = request.GET.get('category_id')
    
    trips = Voyage.objects.all()
    categories = Categorie.objects.all()

    if query:
        trips = trips.filter(
            Q(destination__nom__icontains=query) |
            Q(avion__nomAvion__icontains=query) |
            Q(hotel__hotelNom__icontains=query) |
            Q(description__icontains=query) |
            Q(destination__country__nom__icontains=query) |
            Q(destination__country__categorie__nom__icontains=query)
        )

    if category_id:
        trips = trips.filter(destination__country__categorie__id=category_id)

    if min_price:
        trips = trips.filter(prix__gte=min_price)
    if min_duration:
        trips = trips.filter(duration__gte=min_duration)

    if sort_option == 'price':
        trips = trips.order_by('prix')
    elif sort_option == 'duration':
        trips = trips.order_by('duration')

    max_price = Voyage.objects.aggregate(Max('prix'))['prix__max']
    max_duration = Voyage.objects.aggregate(Max('duration'))['duration__max']
    
    context = {'trips': trips, 'categories': categories, 'max_price': max_price,'max_duration':max_duration}
    
    if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        trips_html = render(request, 'trips/trips_partial.html', context).content.decode('utf-8')
        return JsonResponse({'trips_html': trips_html})

    return render(request, 'trips/Tripsv.html', context)

def country(request, pk):
    country = get_object_or_404(Country, pk=pk)
    voyages = Voyage.objects.filter(country=country)
    context = {'country': country, 'voyages': voyages}
    return render(request, 'trips/Country.html', context)

def destinationDetails(request, pk):
    country = get_object_or_404(Country, pk=pk)
    voyages = Voyage.objects.filter(destination__country=country)
    context = {'country': country, 'voyages': voyages}
    return render(request, 'trips/destinationDetails.html', context)

@login_required(login_url='users:login')
def voyageBooking(request, pk):
    voyage = get_object_or_404(Voyage, pk=pk)

    if request.method == 'POST':
        # Your existing logic to handle the voyage booking form data

        # Payment form handling logic
        holder_name = request.POST.get('holdername')
        card_number = request.POST.get('cardno')
        cvc = request.POST.get('cvcpwd')
        total_str = request.POST.get('MontantTotal')
        total = Decimal(total_str)+Decimal(voyage.prix)

        # Check the selected payment method based on the radio button name
        payment_method = request.POST.get('flexRadioDefault')

        if payment_method == 'visa':  # Adjust the values based on your HTML structure
            try:
                visa_account = CompteVisa.objects.get(nomComplet=holder_name, cardNumber=card_number, code=cvc)
            except CompteVisa.DoesNotExist:
                messages.error(request, 'Invalid payment information. Please check your details and try again.')
                return render(request, 'trips/voyageBooking.html', {'voyage': voyage, 'messages': messages.get_messages(request)})

            # Check if there's enough balance in the Visa account (customize based on your business logic)
            if visa_account.solde < total:
                messages.error(request, 'Insufficient balance in your Visa account.')
                return render(request, 'trips/voyageBooking.html', {'voyage': voyage, 'messages': messages.get_messages(request)})

            visa_account.solde -= total
            visa_account.save()

        elif payment_method == 'paypal':  # Adjust the values based on your HTML structure
            try:
                paypal_account = ComptePayPal.objects.get(nomComplet=holder_name, cardNumber=card_number, code=cvc)
            except ComptePayPal.DoesNotExist:
                messages.error(request, 'Invalid payment information. Please check your details and try again.')
                return render(request, 'trips/voyageBooking.html', {'voyage': voyage, 'messages': messages.get_messages(request)})

            # Check if there's enough balance in the PayPal account (customize based on your business logic)
            if paypal_account.solde < total:
                messages.error(request, 'Insufficient balance in your PayPal account.')
                return render(request, 'trips/voyageBooking.html', {'voyage': voyage, 'messages': messages.get_messages(request)})

            paypal_account.solde -= total
            paypal_account.save()

        # Your existing reservation creation logic
        reservation = Reservation.objects.create(
            voyage=voyage,
            client=request.user,
            nbDePlace=request.POST['totalPersonnes'],
            nbDeChambre=request.POST['totalChambres'],
            prixTotal=total,
        )

        NotificationAdmin.objects.create(
            description="New reservation is added",
            voyage=voyage.destination.nom
        )

        messages.success(request, 'Reservation successful!')
        return redirect('voyageBooking', pk=voyage.id)

    return render(request, 'trips/voyageBooking.html', {'voyage': voyage})

def reservationDetails(request):
    notifications=NotificationClient.objects.all()
    user_id = request.user
    reservations = Reservation.objects.filter(client=user_id)
    return render(request, 'trips/reservationDetails.html',{'reservations':reservations,'notifications':notifications})

def cancelReservation(request,pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    reservation.delete()
    referer = request.META.get('HTTP_REFERER')
    return redirect(referer) 

def infosBanque(request,pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    return render(request, 'trips/infosBanque.html',{'reservation':reservation})

def reverserArgent(request,pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == 'POST':
        # Your existing logic to handle the voyage booking form data

        # Payment form handling logic
        holder_name = request.POST.get('holdername')
        card_number = request.POST.get('cardno')
        cvc = request.POST.get('cvcpwd')
        total = Decimal(reservation.prixTotal)

        # Check the selected payment method based on the radio button name
        payment_method = request.POST.get('flexRadioDefault')

        if payment_method == 'visa':  # Adjust the values based on your HTML structure
            try:
                visa_account = CompteVisa.objects.get(nomComplet=holder_name, cardNumber=card_number, code=cvc)
            except CompteVisa.DoesNotExist:
                messages.error(request, 'Invalid payment information. Please check your details and try again.')
                return render(request, 'trips/infosBanque.html', { 'reservation': reservation,'messages': messages.get_messages(request)})

            visa_account.solde += total
            visa_account.save()

        elif payment_method == 'paypal':  # Adjust the values based on your HTML structure
            try:
                paypal_account = ComptePayPal.objects.get(nomComplet=holder_name, cardNumber=card_number, code=cvc)
            except ComptePayPal.DoesNotExist:
                messages.error(request, 'Invalid payment information. Please check your details and try again.')
                return render(request, 'trips/infosBanque.html', { 'reservation': reservation,'messages': messages.get_messages(request)})
            
            paypal_account.solde+= total
            paypal_account.save()

        reservation.delete()
        
    return redirect('reservationDetails')

def editReservation(request,pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    voyage = reservation.voyage
    prixAncient=reservation.prixTotal

    if request.method == 'POST':
        # Your existing logic to handle the voyage booking form data

        # Payment form handling logic
        holder_name = request.POST.get('holdername')
        card_number = request.POST.get('cardno')
        cvc = request.POST.get('cvcpwd')
        total_str = request.POST.get('MontantTotal')
        total = Decimal(total_str)+Decimal(voyage.prix)

        # Check the selected payment method based on the radio button name
        payment_method = request.POST.get('flexRadioDefault')

        if payment_method == 'visa':  # Adjust the values based on your HTML structure
            try:
                visa_account = CompteVisa.objects.get(nomComplet=holder_name, cardNumber=card_number, code=cvc)
            except CompteVisa.DoesNotExist:
                messages.error(request, 'Invalid payment information. Please check your details and try again.')
                return render(request, 'trips/voyageBooking.html', {'voyage': voyage, 'messages': messages.get_messages(request)})

            # Check if there's enough balance in the Visa account (customize based on your business logic)
            if visa_account.solde < total:
                messages.error(request, 'Insufficient balance in your Visa account.')
                return render(request, 'trips/voyageBooking.html', {'voyage': voyage, 'messages': messages.get_messages(request)})

            visa_account.solde += prixAncient
            visa_account.save()
            visa_account.solde -= total
            visa_account.save()

        elif payment_method == 'paypal':  # Adjust the values based on your HTML structure
            try:
                paypal_account = ComptePayPal.objects.get(nomComplet=holder_name, cardNumber=card_number, code=cvc)
            except ComptePayPal.DoesNotExist:
                messages.error(request, 'Invalid payment information. Please check your details and try again.')
                return render(request, 'trips/editReservation.html', {'reservation': reservation, 'messages': messages.get_messages(request)})

            # Check if there's enough balance in the PayPal account (customize based on your business logic)
            if paypal_account.solde < total:
                messages.error(request, 'Insufficient balance in your PayPal account.')
                return render(request, 'trips/editReservation.html', {'reservation': reservation, 'messages': messages.get_messages(request)})
            paypal_account.solde += prixAncient
            paypal_account.save()
            paypal_account.solde -= total 
            paypal_account.save()


        reservation.voyage=voyage
        reservation.client=request.user
        reservation.nbDePlace=request.POST['totalPersonnes']
        reservation.nbDeChambre=request.POST['totalChambres']
        reservation.prixTotal=total
        reservation.save()


        messages.success(request, 'Reservation successful!')
        return redirect('reservationDetails')

    return render(request, 'trips/editReservation.html', {'reservation': reservation})

def profile(request):
    notifications=NotificationClient.objects.all()
    user = request.user
    return render(request,'trips/profile.html',{'user':user,'notifications':notifications})

def editProfileView(request):
    user = request.user
    return render(request,'trips/editProfile.html',{'user':user})

def saveProfileChange(request):
    user = request.user

    if request.method == 'POST':
        # Update the instance with the submitted data
        user.first_name = request.POST.get('firstName')
        user.last_name = request.POST.get('lastName')
        user.username = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.adresse = request.POST.get('adresse')
        user.photo = request.FILES.get('photo')
        user.save()
        referer = request.META.get('HTTP_REFERER')
        return redirect('profileClient')  # Replace with the actual view name or URL
    else:
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)  # Replace with your template name