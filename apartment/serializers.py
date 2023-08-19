from rest_framework import serializers
from . import models


class ApartmentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ApartmentImage
        fields = ['apartment_id', 'images',]


class ApartmentSerializer(serializers.ModelSerializer):
    maintenance_requests = serializers.IntegerField(read_only=True)
    images = serializers.SerializerMethodField()

    class Meta:
        model = models.Apartment
        fields = ['id', 'owner_id', 'owner_name', 'name', 'status', 'description',
                  'address', 'lga', 'city', 'state',
                  'number_of_occupants', 'number_of_rooms', 'hasOccupants', 'isOccupied',
                  'price', 'apartment_fees', 'amenities', 'rules', 'images',
                  'map_url', 'apartment_type', 'tax', 'tax_price', 'rating',
                  'number_of_reviews', 'total_price', 'created_at', 'updated_at', 'maintenance_requests',
                  'cancellation_policy','has_master_bedroom','credit_renting', 'shared_housing']

    def get_images(self, obj):
        image_fields = ['image1', 'image2', 'image3', 'image4', 'image5']
        images = {}
        for field in image_fields:
            image = getattr(obj, field)
            if image:
                images[field] = image.url
        return images


class ListApartmentSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = models.Apartment
        fields = ['owner_id', 'owner_name', 'name', 'description',
                  'address', 'lga', 'city', 'state',
                  'number_of_rooms', 'price', 'apartment_fees',
                  'amenities', 'rules', 'images', 'map_url', 'apartment_type', 'is_draft',
                  'cancellation_policy','has_master_bedroom','credit_renting', 'shared_housing']

    def get_images(self, obj):
        image_fields = ['image1', 'image2', 'image3', 'image4', 'image5']
        images = {}
        for field in image_fields:
            image = getattr(obj, field)
            if image:
                images[field] = image.url
        return images


class GetApartmentAmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ApartmentAmenities
        fields = ['id', 'amenity']


class GetApartmentRulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ApartmentRules
        fields = ['id', 'rule']


class SaveApartmentDraftSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = models.Apartment
        fields = ['owner_id', 'owner_name', 'name', 'description',
                  'address', 'lga', 'city', 'state',
                  'number_of_rooms', 'price', 'apartment_fees',
                  'amenities', 'rules', 'images', 'map_url', 'apartment_type', 'is_draft']

    def get_images(self, obj):
        image_fields = ['image1', 'image2', 'image3', 'image4', 'image5']
        images = {}
        for field in image_fields:
            image = getattr(obj, field)
            if image:
                images[field] = image.url
        return images


class UnlistApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Apartment
        fields = ['id']


class ApartmentBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ApartmentBooking
        fields = ['apartment_id',
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
        fields = ['name', 'phone_number',
                  'maintenance_category', 'maintenance_type',
                  'description',]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transaction
        fields = ("__all__")
