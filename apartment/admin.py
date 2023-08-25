from django.contrib import admin
from . import models

# Register your models here.


# admin.site.register(models.Apartment)
admin.site.register(models.ApartmentReview)
admin.site.register(models.ApartmentInspection)

admin.site.register(models.Maintenance)



@admin.register(models.ApartmentBooking)
class ApartmentBookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'apartment_id', 'isPaidFor',
                    'user_id',]


@admin.register(models.Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'city', 'is_draft', 'number_of_occupants', 'hasOccupants', 'isOccupied',
                    'rating',]


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'amount', 'transaction_status',
                    'payment_reference', 'created_at', 'updated_at',]

@admin.register(models.ApartmentAmenities)
class ApartmentAmenitiesAdmin(admin.ModelAdmin):
    list_display = ['id', 'amenity']

@admin.register(models.ApartmentRules)
class ApartmentRulesAdmin(admin.ModelAdmin):
    list_display = ['id', 'rule']

@admin.register(models.SaftyAndSecurity)
class SaftyAndSecurityAdmin(admin.ModelAdmin):
    list_display = ['id', 'item']

@admin.register(models.CancellationPolicy)
class CancellationPolicyAdmin(admin.ModelAdmin):
    list_display = ['id', 'policy']

@admin.register(models.AdditionalCharge)
class AdditionalChargeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'amount']
