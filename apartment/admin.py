from django.contrib import admin
from . import models

# Register your models here.


admin.site.register(models.Apartment)
admin.site.register(models.ApartmentImages)
admin.site.register(models.ApartmentReview)
admin.site.register(models.UserData)
admin.site.register(models.ApartmentInspection)





@admin.register(models.ApartmentBooking)
class ApartmentBookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'apartment_id',
                    'user_id',]


# class ApartmentAdmin(admin.ModelAdmin):
