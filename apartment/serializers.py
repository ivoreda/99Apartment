from rest_framework import serializers
from . import models


class ApartmentSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = models.Apartment
        fields = ['id', 'owner_id', 'owner_name', 'name', 'status', 'description',
                  'address', 'city', 'state', 'number_of_occupants', 'number_of_rooms',
                  'number_of_bathrooms', 'number_of_toilets', 'hasOccupants', 'isOccupied',
                  'price', 'owner_price', 'tax', 'tax_price', 'master_bedroom_price', 'master_bedroom_tax_price',
                  'master_bedroom_total_price', 'apartment_fees', 'amenities', 'rules',
                  'cancellation_policy', 'point_of_interest', 'map_url', 'apartment_type',
                  'lease_type',  'rating', 'number_of_reviews', 'total_price',
                  'is_draft', 'images', 'has_master_bedroom',
                  'is_master_bedroom_available', 'credit_renting', 'shared_housing',
                  'created_at', 'updated_at',]

    def get_images(self, obj):
        image_fields = ['image1', 'image2', 'image3', 'image4', 'image5']
        images = {}
        for field in image_fields:
            image = getattr(obj, field)
            if image:
                # Extract the Cloudinary URL from the nested URL
                parts = image.url.split("/media/")
                if len(parts) == 2:
                    images[field] = parts[1]
        return images


class HostApartmentSerializer(serializers.ModelSerializer):
    maintenance_requests = serializers.IntegerField(read_only=True)
    images = serializers.SerializerMethodField()
    maintenance_count = serializers.IntegerField()
    occupancy_rate = serializers.FloatField()
    amount_generated = serializers.DecimalField(
        max_digits=10, decimal_places=2)

    class Meta:
        model = models.Apartment
        fields = ['id', 'owner_id', 'owner_name', 'name', 'status', 'description',
                  'address', 'city', 'state', 'number_of_occupants', 'number_of_rooms',
                  'number_of_bathrooms', 'number_of_toilets', 'hasOccupants', 'isOccupied',
                  'price', 'owner_price', 'tax', 'tax_price', 'total_price', 'master_bedroom_price',
                  'master_bedroom_tax_price', 'master_bedroom_total_price', 'apartment_fees',
                  'amenities', 'rules', 'cancellation_policy', 'point_of_interest', 'map_url',
                  'apartment_type', 'lease_type',  'rating', 'number_of_reviews', 'is_draft',
                  'images', 'maintenance_requests', 'has_master_bedroom',
                  'is_master_bedroom_available', 'credit_renting', 'shared_housing', 'created_at',
                  'updated_at', 'maintenance_count', 'occupancy_rate', 'amount_generated',]

    def get_images(self, obj):
        image_fields = ['image1', 'image2', 'image3', 'image4', 'image5']
        images = {}
        for field in image_fields:
            image = getattr(obj, field)
            if image:
                # Extract the Cloudinary URL from the nested URL
                parts = image.url.split("/media/")
                if len(parts) == 2:
                    images[field] = parts[1]
        return images


class ListApartmentSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = models.Apartment
        fields = ['name', 'status', 'description','address', 'city', 'state', 'number_of_rooms',
                  'number_of_bathrooms', 'number_of_toilets', 'owner_price','master_bedroom_price',
                  'apartment_fees', 'amenities', 'rules', 'cancellation_policy',
                  'point_of_interest', 'map_url', 'apartment_type', 'lease_type', 'is_draft',
                  'images', 'has_master_bedroom', 'is_master_bedroom_available', 'credit_renting',
                  'shared_housing']

    def get_images(self, obj):
        image_fields = ['image1', 'image2', 'image3', 'image4', 'image5']
        images = {}
        for field in image_fields:
            image = getattr(obj, field)
            if image:
                # Extract the Cloudinary URL from the nested URL
                parts = image.url.split("/media/")
                if len(parts) == 2:
                    images[field] = parts[1]
        return images


class GetApartmentAmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ApartmentAmenities
        fields = ['id', 'amenity']


class GetApartmentRulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ApartmentRules
        fields = ['id', 'rule']


class GetSaftyAndSecuritySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SaftyAndSecurity
        fields = ['id', 'item']


class GetAdditionalChargesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AdditionalCharge
        fields = ['id', 'name', 'amount']


class GetCancellationPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CancellationPolicy
        fields = ['id', 'policy']


class SaveApartmentDraftSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = models.Apartment
        fields = ['name', 'status', 'description',
                  'address', 'city', 'state', 'number_of_rooms',
                  'number_of_bathrooms', 'number_of_toilets', 'owner_price', 
                  'apartment_fees', 'amenities', 'rules', 'cancellation_policy',
                  'point_of_interest', 'map_url', 'apartment_type', 'lease_type', 'is_draft',
                  'images', 'has_master_bedroom', 'credit_renting',
                  'shared_housing']

    def get_images(self, obj):
        image_fields = ['image1', 'image2', 'image3', 'image4', 'image5']
        images = {}
        for field in image_fields:
            image = getattr(obj, field)
            if image:
                # Extract the Cloudinary URL from the nested URL
                parts = image.url.split("/media/")
                if len(parts) == 2:
                    images[field] = parts[1]
        return images


class UnlistApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Apartment
        fields = ['id']


class ApartmentBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ApartmentBooking
        fields = ['apartment_id',
                  'paid_for_master_bedroom',
                  'start_date',
                  'no_of_guests',
                  'end_date']


class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ApartmentBooking
        fields = ['apartment_id', 'isPaidFor', 'amount_paid',
                  'user_id', 'payment_link', 'email', 'first_name',
                  'last_name', 'phone_number', 'start_date',
                  'end_date', 'payment_reference', 'cover_photo', 'no_of_guests']


class VerifyApartmentBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ApartmentBooking
        fields = ['payment_reference']


class ResponseSerializer(serializers.Serializer):
    status = serializers.BooleanField(default=True)
    message = serializers.CharField(default='Data retrieved successfully')
    data = ApartmentSerializer(many=True)


class ApartmentInsectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ApartmentInspection
        fields = ['id', 'apartment_id',
                  'user_id',
                  'inspection_date',
                  'inspection_time',
                  'isInspected',
                  'created_at',
                  'updated_at',]


class BookApartmentInsectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ApartmentInspection
        fields = ['apartment_id',
                  'inspection_date',
                  'inspection_time',
                  ]


class ApartmentInsectionResponseSerializer(serializers.Serializer):
    status = serializers.BooleanField(default=True)
    message = serializers.CharField(default='Data retrieved successfully')
    data = ApartmentInsectionSerializer(many=True)


class ApartmentReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ApartmentReview
        fields = ['apartment_id', 'review', 'rating',]


class GetApartmentReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ApartmentReview
        fields = ['id', 'apartment_id', 'user_id',
                  'review', 'rating', 'created_at',]


class ApartmentCitiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Apartment
        fields = ['city']


class MaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Maintenance
        fields = ['user_id', 'name', 'phone_number', 'apartment_id',
                  'maintenance_category', 'maintenance_type',
                  'status', 'description', 'cost',
                  'date_of_complaint', 'time_of_complaint',]


class MaintenanceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Maintenance
        fields = ['maintenance_category', 'maintenance_type',
                  'description',]


class HostMaintenanceSerializer(serializers.ModelSerializer):
    apartment_detail = serializers.SerializerMethodField()

    class Meta:
        model = models.Maintenance
        fields = ['apartment_detail', 'user_id', 'name', 'phone_number',
                  'apartment_id', 'maintenance_category', 'maintenance_type',
                  'priority', 'status', 'description', 'cost',
                  'date_of_complaint', 'time_of_complaint',]

    def get_apartment_detail(self, obj):
        return obj.apartment_id.name


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transaction
        fields = ("__all__")


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Service
        fields = '__all__'


class ChangeApartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ChangeApartment
        fields = ['budget', 'current_apartment', 'preferred_space',
                  'budget', 'preferred_facilities', 'reason_for_change',]
