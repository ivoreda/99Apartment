from django.contrib import admin
from . import models

# Register your models here.


admin.site.register(models.Apartment)
admin.site.register(models.ApartmentImages)
admin.site.register(models.ApartmentReviews)
admin.site.register(models.UserData)
admin.site.register(models.ApartmentInspection)
admin.site.register(models.ApartmentBooking)





# class ApartmentAdmin(admin.ModelAdmin):
