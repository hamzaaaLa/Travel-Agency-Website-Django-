from django.contrib import admin
from .models import Categorie
from .models import Country
from .models import Voyage
from .models import Avion
from .models import Hotel
from .models import Destination

admin.site.register(Voyage)
admin.site.register(Avion)
admin.site.register(Hotel)
admin.site.register(Destination)
admin.site.register(Categorie)
admin.site.register(Country)
# Register your models here.
