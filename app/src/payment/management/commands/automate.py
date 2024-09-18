from concurrent.futures import ThreadPoolExecutor
from django.core.management.base import BaseCommand
from payment.utils import RakBankManager  # Import other managers as needed
from payment.models import PaymentLink, PaymentMethod, PersonalInfo, PaymentCount


class Command(BaseCommand):
    help = "Automates the payment process for multiple URLs concurrently."

    def handle(self, *args, **kwargs):
        # Fetch active payment links and required personal info
        personal_info = PersonalInfo.objects.first()

        # Fetch the payment count limit from PaymentCount model
        try:
            payment_count = (
                PaymentCount.objects.first().count
            )  # Get the count from the model
        except AttributeError:
            self.stdout.write(
                self.style.ERROR(
                    "No PaymentCount record found. Please set a valid count."
                )
            )
            return

        # Fetch the payment links up to the limit specified by payment_count
        payment_links = PaymentLink.objects.filter(active=True)[:payment_count]

        # Define the automation logic for each payment link
        def automate_link(payment_link):
            try:
                # Dynamically load the correct payment manager based on the website
                if payment_link.website == "rakbank":
                    manager = RakBankManager(
                        payment_link, personal_info, payment_link.payment_method
                    )
                else:
                    # Placeholder for future payment managers
                    self.stdout.write(
                        f"No manager defined for {payment_link.website}. Skipping."
                    )
                    return

                # Automate the payment process
                manager.automate_payment()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully automated payment for {payment_link.short_name}"
                    )
                )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Error automating payment for {payment_link.short_name}: {e}"
                    )
                )

        # Execute the automation concurrently using ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(automate_link, link) for link in payment_links]

        # Ensure all tasks are completed
        for future in futures:
            try:
                future.result()  # This will raise exceptions if any occurred during execution
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error in thread: {e}"))
