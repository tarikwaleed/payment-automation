
from django.contrib import admin
from .models import PaymentLink, PaymentMethod, PersonalInfo, PaymentCount, PaymentAssociation,ScreenshotPath,CSVFilePath

@admin.register(PaymentLink)
class PaymentLinkAdmin(admin.ModelAdmin):
    list_display = ('url', 'website')

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('card_number', 'expiry_date', 'active')
    list_filter = ('active',)
    search_fields = ('card_number',)

@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'city')
    search_fields = ('name', 'city')

@admin.register(PaymentCount)
class PaymentCountAdmin(admin.ModelAdmin):
    list_display = ('count',)

@admin.register(PaymentAssociation)
class PaymentAssociationAdmin(admin.ModelAdmin):
    list_display = ('payment_method', 'payment_link')
    search_fields = ('payment_method__card_number', 'payment_link__website')

@admin.register(ScreenshotPath)
class ScreenshotPathAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if ScreenshotPath.objects.count() >= 1:
            return False
        return super().has_add_permission(request)


@admin.register(CSVFilePath)
class CSVFilePathAdmin(admin.ModelAdmin):
    list_display = ('path',)
