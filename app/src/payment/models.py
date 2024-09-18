from django.db import models
from django.core.exceptions import ValidationError

class PaymentMethod(models.Model):
    card_number = models.CharField(max_length=16)
    expiry_date = models.CharField(max_length=5)
    cvv = models.CharField(max_length=4)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.card_number[-4:]} - Active: {self.active}"

class PaymentLink(models.Model):
    RAKBANK = 'rakbank'
    OTHER = 'other'
    
    WEBSITE_CHOICES = [
        (RAKBANK, 'RakBank'),
        (OTHER, 'Other'),  # You can add more websites here as needed
    ]
    
    url = models.URLField(max_length=255)
    website = models.CharField(max_length=100, choices=WEBSITE_CHOICES, default=RAKBANK)
    short_name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, related_name='payment_links')

    def __str__(self):
        return self.short_name




class PersonalInfo(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if PersonalInfo.objects.exists() and not self.pk:
            # If a record already exists and this is a new instance (no primary key yet)
            raise ValueError("Only one PersonalInfo instance is allowed.")
        super(PersonalInfo, self).save(*args, **kwargs)

class PaymentCount(models.Model):
    count = models.PositiveIntegerField()

    def __str__(self):
        return f"Payment Count: {self.count}"


class PaymentAssociation(models.Model):
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    payment_link = models.ForeignKey(PaymentLink, on_delete=models.CASCADE)

    def __str__(self):
        return f"Association: {self.payment_method} with {self.payment_link}"


class ScreenshotPath(models.Model):
    path = models.CharField(max_length=255, help_text="Path to store screenshots")

    def clean(self):
        # Ensure that only one record can be created
        if ScreenshotPath.objects.exists() and not self.pk:
            raise ValidationError("Only one ScreenshotPath instance is allowed.")

    def __str__(self):
        return self.path

class CSVFilePath(models.Model):
    path = models.CharField(max_length=255, help_text="Path to the CSV file")

    def clean(self):
        # Ensure that only one record can be created
        if CSVFilePath.objects.exists() and not self.pk:
            raise ValidationError("Only one CSVFilePath instance is allowed.")

    def __str__(self):
        return self.path
