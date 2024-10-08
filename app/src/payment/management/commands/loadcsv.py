
import csv
from django.core.management.base import BaseCommand
from payment.models import PaymentLink, PaymentMethod, CSVFilePath  # Ensure CSVFilePath is correctly imported
from django.core.exceptions import ObjectDoesNotExist  # Generic exception for DoesNotExist

class Command(BaseCommand):
    help = 'Populate PaymentLink table from CSV file specified in the database.'

    def handle(self, *args, **kwargs):
        csv_file_path=''
        try:
            # Get the CSV file path from the database
            csv_file_record = CSVFilePath.objects.get()  # Assumes only one record is allowed
            csv_file_path = csv_file_record.path

            # Open the CSV file and read it
            with open(csv_file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                # Iterate through the rows in the CSV and create/update PaymentLink records
                for row in reader:
                    url = row['url']
                    website = row['website']
                    short_name = row['short_name']
                    active = row['active'].lower() in ('true', '1', 'yes')  # Handle boolean
                    payment_method_id = row.get('payment_method_id')

                    # Fetch the payment method from the database
                    try:
                        payment_method = PaymentMethod.objects.get(id=payment_method_id)
                    except PaymentMethod.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f'PaymentMethod with ID {payment_method_id} does not exist. Skipping {short_name}.'))
                        continue  # Skip to the next row if the PaymentMethod is not found

                    # Create or update the PaymentLink record
                    # obj, created = PaymentLink.objects.update_or_create(
                    #     url=url,
                    #     defaults={
                    #         'website': website,
                    #         'short_name': short_name,
                    #         'active': active,
                    #         'payment_method': payment_method,  # Link to the payment method
                    #     }
                    # )
                    try:
                        PaymentLink.objects.create(
                                url=url,
                                website=website,
                                short_name=short_name,
                                active=active,
                                payment_method=payment_method,  # Link to the payment method
                            )

                        self.stdout.write(self.style.SUCCESS(f'Created PaymentLink: {short_name}'))
                    except:
                        self.stdout.write(self.style.SUCCESS(f'Updated PaymentLink: {short_name}'))

        except ObjectDoesNotExist:
            self.stdout.write(self.style.ERROR('No CSVFilePath record found in the database.'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File {csv_file_path} not found.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error reading file {csv_file_path}: {e}'))
