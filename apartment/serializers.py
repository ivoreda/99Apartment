from rest_framework import serializers
from . import models


class ApartmentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ApartmentImage
        fields = ['apartment_id','image',]


class ApartmentSerializer(serializers.ModelSerializer):
    image = ApartmentImageSerializer(many=True, read_only=True)

    class Meta:
        model = models.Apartment
        fields = ['id',
                  'name',
                  'description',
                  'address',
                  'lga',
                  'city',
                  'state',
                  'country',
                  'number_of_occupants',
                  'number_of_rooms',
                  'hasOccupants',
                  'isOccupied',
                  'price',
                  'apartment_fees',
                  'amenities',
                  'rules',
                  'map_url',
                  'apartment_type',
                  'tax',
                  'rating',
                  'number_of_reviews',
                  'image',
                  'total_price',
                  'created_at',
                  'updated_at',]


class ApartmentBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ApartmentBooking
        fields = ['apartment_id',
                  'start_date',
                  'end_date']


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
