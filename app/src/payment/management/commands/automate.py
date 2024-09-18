from concurrent.futures import ThreadPoolExecutor
from django.core.management.base import BaseCommand
from payment.utils import RakBankManager
from payment.models import PaymentLink, PaymentMethod, PersonalInfo  

class Command(BaseCommand):
    help = 'Automates the payment process for multiple URLs concurrently.'

    def handle(self, *args, **kwargs):
        payment_links = PaymentLink.objects.filter(active=True)
        personal_info = PersonalInfo.objects.first()  
        payment_method = PaymentMethod.objects.filter(active=True).first()  

        def automate_link(payment_link):
            if payment_link.website == 'rakbank':
                manager = RakBankManager( payment_link, personal_info, payment_method)
                manager.automate_payment()

        with ThreadPoolExecutor(max_workers=5) as executor:  
            futures = [executor.submit(automate_link, link) for link in payment_links]

        for future in futures:
            future.result()  
