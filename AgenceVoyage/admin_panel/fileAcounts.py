from models import ComptePayPal
from models import CompteVisa

# Remplissage du modèle CompteVisa
visa1 = CompteVisa.objects.create(nomComplet="Ahmed Abdou", cardNumber="1234-5678-9999", code="123", solde=100000.00)
visa2 = CompteVisa.objects.create(nomComplet="Amina El", cardNumber="1111-2222-3333-4444", code="456", solde=2000.00)

# Remplissage du modèle ComptePayPal
paypal1 = ComptePayPal.objects.create(nomComplet="Amine El", cardNumber="1111-2222-3333-4444", code="789", solde=3000.00)
paypal2 = ComptePayPal.objects.create(nomComplet="Sanae El", cardNumber="1111-1111-1111-1111", code="12345", solde=4000.00)