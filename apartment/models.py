from django.db import models
from cloudinary.models import CloudinaryField
from decimal import Decimal


# Create your models here.


class Apartment(models.Model):
    """Model for Apartment"""

    LEASE_TYPE = (('Short Lease', 'Short Lease'),
                  ('Long Lease', 'Long Lease'))

    APARTMENT_STATUS = (('Listed', 'Listed'),
                        ('Unlisted', 'Unlisted'),
                        ('Pending', 'Pending'),
                        # ('Unverified', 'Unverified'),
                        # ('Verified', 'Verified'),
                        ('Draft', 'Draft'),)

    APARTMENT_VERIFICATION_STATUS = (('Pending', 'Pending'),
                                     ('Unverified', 'Unverified'),
                                     ('Verified', 'Verified'),)

    owner_id = models.CharField(
        max_length=255, help_text='Apartment owner ID', default='owner ID')
    owner_name = models.CharField(
        max_length=255, help_text='Apartment owner name', default='owner name')
    name = models.CharField(max_length=255, help_text="Apartment name")
    status = models.CharField(
        max_length=255, choices=APARTMENT_STATUS, default='Unverified')
    description = models.TextField(help_text="Enter apartment description")
    address = models.TextField(help_text="Enter apartment address")
    city = models.CharField(max_length=50, help_text="City")
    state = models.CharField(max_length=20, help_text="State")

    number_of_occupants = models.IntegerField(default=0)
    number_of_rooms = models.IntegerField(default=0)
    number_of_bathrooms = models.IntegerField(default=0)
    number_of_toilets = models.IntegerField(default=0)
    hasOccupants = models.BooleanField(default=False)
    isOccupied = models.BooleanField(default=False)
    _occupancy_rate = models.FloatField(default=0.0)

    # owner_price field for the owner to add,
    owner_price = models.IntegerField(
        default=0)

    # admin will edit this price
    price = models.IntegerField(default=10)

    master_bedroom_price = models.IntegerField(
        default=0)
    master_bedroom_tax_price = models.IntegerField(
        default=0)
    master_bedroom_total_price = models.IntegerField(
        default=0)

    rooms = models.JSONField(default=[])

    apartment_fees = models.JSONField(default=dict, blank=True, null=True)
    amenities = models.JSONField(
        default=[], blank=True, null=True)
    rules = models.JSONField(default=[], blank=True, null=True)
    safty_and_security = models.JSONField(default=[], blank=True, null=True)
    cancellation_policy = models.JSONField(default=[], blank=True, null=True)
    point_of_interest = models.TextField(default='')

    map_url = models.TextField(default="map url", blank=True, null=True)
    apartment_type = models.CharField(default='', max_length=255)
    lease_type = models.CharField(default='Long Lease', choices=LEASE_TYPE)
    tax = models.FloatField(default=7.5)
    master_bedroom_percentage = models.FloatField(
        default=0.3)
    tax_price = models.IntegerField(
        default=0)
    rating = models.DecimalField(default=0.0, decimal_places=1, max_digits=10)
    number_of_reviews = models.IntegerField(default=0)

    image1 = models.ImageField(
        upload_to='apartment-images/', blank=True, null=True)
    image2 = models.ImageField(
        upload_to='apartment-images/', blank=True, null=True)
    image3 = models.ImageField(
        upload_to='apartment-images/', blank=True, null=True)
    image4 = models.ImageField(
        upload_to='apartment-images/', blank=True, null=True)
    image5 = models.ImageField(
        upload_to='apartment-images/', blank=True, null=True)

    total_price = models.IntegerField(
        default=0)

    single_room_total_price = models.IntegerField(
        default=0)

    is_draft = models.BooleanField(default=False)

    # verification_status = models.CharField(
    #     choices=APARTMENT_VERIFICATION_STATUS, default='Unverified')

    is_master_bedroom_available = models.BooleanField(default=True)
    has_master_bedroom = models.BooleanField(default=False)
    credit_renting = models.BooleanField(default=False)
    shared_housing = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    def calculate_occupancy_rate(self):
        # Calculate the occupancy rate based on your criteria
        # For example, you can count the number of occupied units and divide by the total number of units.
        total_units = self.number_of_rooms  # Replace with your actual field name
        occupied_units = self.number_of_occupants  # Replace with your actual field name
        if total_units == 0:
            return 0  # Avoid division by zero
        return (occupied_units / total_units) * 100

    # Define a property for occupancy_rate
    @property
    def occupancy_rate(self):
        return self.calculate_occupancy_rate()

    @occupancy_rate.setter
    def occupancy_rate(self, value):
        # You can add custom logic here if you want to set the occupancy rate
        # For example, you might want to update other fields based on the rate.
        # For this example, we'll just set the rate directly.
        self._occupancy_rate = value

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
        self.tax_price = round(
            self.price / self.number_of_rooms) * self.tax / 100
        self.total_price = (self.tax_price * self.number_of_rooms) + \
            self.price + (sum(total_apartment_fees) * self.number_of_rooms)

        self.single_room_total_price = self.tax_price + \
            round(self.price / self.number_of_rooms) + \
            sum(total_apartment_fees)

        if self.has_master_bedroom:
            self.master_bedroom_price = (
                (self.price/self.number_of_rooms) * self.master_bedroom_percentage) + (self.price/self.number_of_rooms)
            self.master_bedroom_tax_price = round(
                self.master_bedroom_price * self.tax / 100)
            self.master_bedroom_total_price = self.master_bedroom_tax_price + \
                self.master_bedroom_price + sum(total_apartment_fees)

        self.rooms = []

        for i in range(1, self.number_of_rooms):
            room = {'id': i, 'price': round(self.price/self.number_of_rooms),
                    'total_price': round(self.single_room_total_price),
                    'tax': round(self.tax_price), 'apartment_fees': self.apartment_fees}
            self.rooms.append(room)
        super(Apartment, self).save(*args, **kwargs)


class ApartmentBooking(models.Model):
    apartment_id = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    isPaidFor = models.BooleanField(default=False)
    paid_for_master_bedroom = models.BooleanField(default=False)
    amount_paid = models.IntegerField(
        default=0)
    user_id = models.CharField(max_length=255)
    payment_link = models.CharField(max_length=255, default='payment link')
    email = models.EmailField(default='email')
    first_name = models.CharField(default='first name')
    last_name = models.CharField(default='last name')
    phone_number = models.CharField(default='phone number')
    start_date = models.DateField()
    end_date = models.DateField()
    payment_reference = models.CharField(max_length=255)
    no_of_rooms = models.IntegerField(default=1)
    cover_photo = models.TextField(default='photo')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user_id


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
                        ('Maintenance', 'Maintenance'),)

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
                        ('Structural', 'Structural'),
                        ('Plumbing', 'Plumbing'),)

    MAINTENANCE_CATEGORY = (('Routine', 'Routine'),
                            ('Emergency', 'Emergency'),)

    MAINTENANCE_STATUS = (('Pending', 'Pending'),
                          ('In Progress', 'In Progress'),
                          ('Done', 'Done'),)

    PRIORITY_LEVEL = (('Low', 'Low'),
                      ('Medium', 'Medium'),
                      ('High', 'High'))

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
    priority = models.CharField(choices=PRIORITY_LEVEL, default='Low')
    description = models.TextField()
    cost = models.IntegerField(default=0)
    date_of_complaint = models.DateField(auto_now_add=True)
    time_of_complaint = models.TimeField(auto_now_add=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Maintenance request from '{self.name}'"


class Service(models.Model):
    SERVICE_PAYMENT_STATUS = (('Pending', 'Pending'),
                              ('Paid', 'Paid'),)

    apartment_id = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    transaction_date = models.DateField(auto_now_add=True)
    transaction_time = models.TimeField(auto_now_add=True)
    expense = models.CharField(max_length=255)
    status = models.CharField(
        choices=SERVICE_PAYMENT_STATUS, default='Pending')
    amount = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.expense


class ApartmentAmenities(models.Model):
    amenity = models.CharField(max_length=500)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.amenity


class ApartmentRules(models.Model):
    rule = models.CharField(max_length=500)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.rule


class SaftyAndSecurity(models.Model):
    item = models.CharField(max_length=500)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.item


class CancellationPolicy(models.Model):
    policy = models.CharField(max_length=500)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.policy


class AdditionalCharge(models.Model):
    name = models.CharField(max_length=500, default='charge')
    amount = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class ChangeApartment(models.Model):
    resident_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)

    current_apartment = models.ForeignKey(
        Apartment, on_delete=models.CASCADE, related_name='current_apartment_changes')

    preferred_space = models.CharField(max_length=20)

    budget = models.CharField(max_length=15)
    preferred_facilities = models.TextField()
    reason_for_change = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.resident_name


class ChangeApartmentNotification(models.Model):
    resident_name = models.CharField(max_length=30)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.resident_name
