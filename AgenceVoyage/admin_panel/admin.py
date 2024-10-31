from django.contrib import admin
from .models import Categorie
from .models import Country
from .models import Voyage
from .models import Avion
from .models import Hotel
from .models import Destination
from .models import ComptePayPal
from .models import CompteVisa
from .models import Reservation
from .models import Promotion
from .models import NotificationClient
from .models import NotificationAdmin


admin.site.register(NotificationAdmin)
admin.site.register(NotificationClient)
admin.site.register(Promotion)
admin.site.register(Reservation)
admin.site.register(CompteVisa)
admin.site.register(ComptePayPal)
admin.site.register(Voyage)
admin.site.register(Avion)
admin.site.register(Hotel)
admin.site.register(Destination)
admin.site.register(Categorie)
admin.site.register(Country)
# Register your models here.
