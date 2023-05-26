from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.


class Apartment(models.Model):
    """Model for Apartment"""

    APARTMENT_TYPE = (('Shared Housing', 'Shared Housing'),
                      ('Credit Renting', 'Credit Renting'),)


    name = models.CharField(max_length=255, help_text="Apartment name")
    description = models.TextField(help_text="Enter apartment description")
    address = models.TextField(help_text="Enter apartment address")
    lga = models.CharField(max_length=50, help_text="LGA")
    city = models.CharField(max_length=50, help_text="City")
    state = models.CharField(max_length=20, help_text="State")
    country = models.CharField(max_length=50, help_text="Country")
    number_of_occupants = models.IntegerField(default=0)
    number_of_rooms = models.IntegerField(default=0)
    hasOccupants = models.BooleanField(default=False)
    isOccupied = models.BooleanField(default=False)
    price = models.IntegerField(default=0)

    image1 = CloudinaryField('image 1', null=True, default=None, blank=True)
    image2 = CloudinaryField('image 2', null=True, default=None, blank=True)
    image3 = CloudinaryField('image 3', null=True, default=None, blank=True)
    image4 = CloudinaryField('image 4', null=True, default=None, blank=True)
    image5 = CloudinaryField('image 5', null=True, default=None, blank=True)
    image6 = CloudinaryField('image 6', null=True, default=None, blank=True)
    image7 = CloudinaryField('image 7', null=True, default=None, blank=True)
    image8 = CloudinaryField('image 8', null=True, default=None, blank=True)
    image9 = CloudinaryField('image 9', null=True, default=None, blank=True)
    image10 = CloudinaryField('image 10', null=True, default=None, blank=True)

    apartment_fees = models.JSONField(default=dict, blank=True, null=True)
    amenities = models.JSONField(default=dict, blank=True, null=True)
    rules = models.JSONField(default=dict, blank=True, null=True)
    map_url = models.TextField(default= "map url", blank=True, null=True)
    apartment_type = models.CharField(choices=APARTMENT_TYPE, default='Shared Housing', blank=True, null=True, max_length=255)
    tax = models.DecimalField(default=0.0, decimal_places=1, max_digits=10)
    rating = models.DecimalField(default=0.0, decimal_places=1, max_digits=10)
    number_of_reviews = models.IntegerField(default=0)

    total_price = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if self.number_of_rooms == self.number_of_occupants:
            self.isOccupied = True
        else:
            self.isOccupied = False
        if self.number_of_occupants >= 1:
            self.hasOccupants = True
        else:
            self.hasOccupants = False
        super(Apartment, self).save(*args, **kwargs)


class ApartmentImages(models.Model):
    """
    images are uploaded to cloudinary or S3
    and the links are saved
    """
    apartment_id = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    image1 = CloudinaryField('image 1', null=True, default=None, blank=True)
    image2 = CloudinaryField('image 2', null=True, default=None, blank=True)
    image3 = CloudinaryField('image 3', null=True, default=None, blank=True)
    image4 = CloudinaryField('image 4', null=True, default=None, blank=True)
    image5 = CloudinaryField('image 5', null=True, default=None, blank=True)
    image6 = CloudinaryField('image 6', null=True, default=None, blank=True)
    image7 = CloudinaryField('image 7', null=True, default=None, blank=True)
    image8 = CloudinaryField('image 8', null=True, default=None, blank=True)
    image9 = CloudinaryField('image 9', null=True, default=None, blank=True)
    image10 = CloudinaryField('image 10', null=True, default=None, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.apartment_id)


class ApartmentBooking(models.Model):
    apartment_id = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    isPaidFor = models.BooleanField(default=False)
    user_id = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    payment_reference = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user_id


class UserData(models.Model):
    """Model for extra user data that is saved on DB"""
    pass


class ApartmentReview(models.Model):
    """Model for apartment reviews"""
    apartment_id = models.ForeignKey(
        Apartment, on_delete=models.CASCADE, default=0)
    user_id = models.CharField(max_length=255)
    review = models.TextField()
    rating = models.DecimalField(default=0.0, decimal_places=1, max_digits=10)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.apartment_id)


class ApartmentInspection(models.Model):
    apartment_id = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=10)
    inspection_date = models.DateField()
    inspection_time = models.TimeField()
    isInspected = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.apartment_id)


class Transaction(models.Model):
    user_id = models.CharField(max_length=10)
    amount = models.CharField(max_length=10)
    transaction_status = models.CharField(max_length=10)
    description = models.CharField(max_length=20)
    recipient = models.CharField(max_length=255)
    payment_reference = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=40)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.user_id)