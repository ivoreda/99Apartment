from django.db import models

# Create your models here.

class Apartment(models.Model):
    """Model for Apartment"""
    name = models.CharField(max_length=255,help_text="Apartment name")
    description = models.TextField(help_text="Enter apartment description")
    address = models.TextField(help_text="Enter apartment address")
    lga = models.CharField(max_length=50,help_text="LGA")
    city = models.CharField(max_length=50,help_text="City")
    state = models.CharField(max_length=20,help_text="State")
    country = models.CharField(max_length=50,help_text="Country")
    number_of_occupants = models.IntegerField(default=0)
    hasOccupants = models.BooleanField(default=False)
    isOccupied = models.BooleanField(default=False)
    price = models.IntegerField(default=0)

    apartment_fees = models.JSONField(blank=True, null=True)
    amenities = models.JSONField(blank=True, null=True)

    total_price = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.name

class ApartmentImages(models.Model):
    """
    images are uploaded to cloudinary or S3
    and the links are saved
    """
    apartment_id = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    image1 = models.TextField()
    image2 = models.TextField()
    image3 = models.TextField()
    image4 = models.TextField()
    image5 = models.TextField()
    image6 = models.TextField()
    image7 = models.TextField()
    image8 = models.TextField()
    image9 = models.TextField()
    image10 = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.apartment_id


class ApartmentBooking(models.Model):
    apartment_id = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    isPaidFor = models.BooleanField(default=False)
    user_id = models.CharField(max_length=10)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    payment_reference = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user_id



class UserData(models.Model):
    """Model for extra user data that is saved on DB"""
    pass

class ApartmentReviews(models.Model):
    """Model for apartment reviews"""
    pass

class ApartmentInspection(models.Model):
    apartment_id = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=10)
    inspection_date = models.DateTimeField()
    isInspected = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.apartment_id)