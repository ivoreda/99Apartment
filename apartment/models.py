from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.


class Apartment(models.Model):
    """Model for Apartment"""

    APARTMENT_TYPE = (('Shared Housing', 'Shared Housing'),
                      ('Credit Renting', 'Credit Renting'),)

    LEASE_TYPE = (('Short Lease', 'Short Lease'),
                  ('Long Lease', 'Long Lease'))

    APARTMENT_STATUS = (('Listed', 'Listed'),
                        ('Unlisted', 'Unlisted'),)

    owner_id = models.CharField(
        max_length=255, help_text='Apartment owner ID', default='owner ID')
    owner_name = models.CharField(
        max_length=255, help_text='Apartment owner name', default='owner name')
    name = models.CharField(max_length=255, help_text="Apartment name")
    status = models.CharField(max_length=255, choices=APARTMENT_STATUS, default='Unlisted')
    description = models.TextField(help_text="Enter apartment description")
    address = models.TextField(help_text="Enter apartment address")
    lga = models.CharField(max_length=50, help_text="LGA")
    city = models.CharField(max_length=50, help_text="City")
    state = models.CharField(max_length=20, help_text="State")

    number_of_occupants = models.IntegerField(default=0)
    number_of_rooms = models.IntegerField(default=0)
    number_of_bathrooms = models.IntegerField(default=0)
    number_of_toilets = models.IntegerField(default=0)
    type_of_space = models.CharField(default='One Bedroom', max_length=40)
    hasOccupants = models.BooleanField(default=False)
    isOccupied = models.BooleanField(default=False)
    price = models.IntegerField(default=0)

    apartment_fees = models.JSONField(default=dict, blank=True, null=True)
    amenities = models.JSONField(
        default=[], blank=True, null=True)
    rules = models.JSONField(default=[], blank=True, null=True)

    map_url = models.TextField(default="map url", blank=True, null=True)
    apartment_type = models.CharField(
        choices=APARTMENT_TYPE, default='Shared Housing', blank=True, null=True, max_length=255)
    tax = models.DecimalField(default=7.5, decimal_places=1, max_digits=10)
    tax_price = models.DecimalField(default=0, decimal_places=1, max_digits=10)
    rating = models.DecimalField(default=0.0, decimal_places=1, max_digits=10)
    number_of_reviews = models.IntegerField(default=0)


    image1 = models.ImageField(upload_to='apartment-images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='apartment-images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='apartment-images/', blank=True, null=True)
    image4 = models.ImageField(upload_to='apartment-images/', blank=True, null=True)
    image5 = models.ImageField(upload_to='apartment-images/', blank=True, null=True)

    total_price = models.IntegerField(default=0)
    is_draft = models.BooleanField(default=False)
    cancellation_policy = models.TextField(default="")

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
        total_apartment_fees = [int(value)
                                for value in self.apartment_fees.values()]
        self.tax_price = self.price * self.tax / 100
        self.total_price = self.tax_price + \
            self.price + sum(total_apartment_fees)
        super(Apartment, self).save(*args, **kwargs)


class ApartmentImage(models.Model):
    """
    images are uploaded to cloudinary or S3
    and the links are saved
    """
    apartment_id = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    images = models.JSONField(default={"images": []}, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.apartment_id)


class ApartmentBooking(models.Model):
    apartment_id = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    isPaidFor = models.BooleanField(default=False)
    amount_paid = models.IntegerField(default=0)
    user_id = models.CharField(max_length=255)
    payment_link = models.CharField(max_length=255, default='payment link')
    email = models.EmailField(default='email')
    first_name = models.CharField(default='first name')
    last_name = models.CharField(default='last name')
    phone_number = models.CharField(default='phone number')
    start_date = models.DateField()
    end_date = models.DateField()
    payment_reference = models.CharField(max_length=255)
    no_of_guests = models.IntegerField(default=1)
    cover_photo = models.TextField(default='photo')

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
    username = models.CharField(default='username')
    user_photo = models.CharField(default='user photo')
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
    inspection_time = models.CharField(max_length=30)
    isInspected = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.apartment_id)


class Transaction(models.Model):

    TRANSACTION_TYPE = (('Annual Rent', 'Annual Rent'),
                        ('Maintainance', 'Maintainance'),)

    TRANSACTION_STATUS = (('Pending', 'Pending'),
                          ('Done', 'Done'),)

    user_id = models.CharField(max_length=10)
    amount = models.CharField(max_length=10)
    transaction_status = models.CharField(
        choices=TRANSACTION_STATUS, max_length=10, default='Pending')
    description = models.TextField(default='description')
    transaction_type = models.CharField(
        choices=TRANSACTION_TYPE, max_length=30, default='Annual Rent')
    recipient = models.CharField(max_length=255)
    payment_reference = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=40)
    transaction_date = models.DateField(auto_now_add=True)
    transaction_time = models.TimeField(auto_now_add=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.user_id)


class Maintenance(models.Model):

    MAINTENANCE_TYPE = (('Electrical', 'Electrical'),
                        ('Structural', 'Structural'),)

    MAINTENANCE_CATEGORY = (('Routine', 'Routine'),
                            ('Emergency', 'Emergency'),)

    MAINTENANCE_STATUS = (('Pending', 'Pending'),
                          ('Done', 'Done'),)

    user_id = models.CharField(max_length=10)
    apartment_id = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=11)
    maintenance_category = models.CharField(
        choices=MAINTENANCE_CATEGORY, max_length=20, default='Routine')
    maintenance_type = models.CharField(
        choices=MAINTENANCE_TYPE, max_length=20, default='Structural')
    status = models.CharField(
        choices=MAINTENANCE_STATUS, max_length=20, default='Pending')
    description = models.TextField()
    cost = models.IntegerField(default=0)
    date_of_complaint = models.DateField(auto_now_add=True)
    time_of_complaint = models.TimeField(auto_now_add=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"maintainance request from '{self.name}'"


# class Service(models.Model):
#     SERVICE_PAYMENT_STATUS = (('Pending', 'Pending'),
#                           ('Paid', 'Paid'),)




class ApartmentAmenities(models.Model):
    amenity = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.amenity


class ApartmentRules(models.Model):
    rule = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.rule

