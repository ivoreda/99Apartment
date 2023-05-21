from rest_framework import serializers
from . import models


class ApartmentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ApartmentImages
        fields = ['apartment_id',
                  'image1',
                  'image2',
                  'image3',
                  'image4',
                  'image5',
                  'image6',
                  'image7',
                  'image8',
                  'image9',
                  'image10',
                  ]


class ApartmentSerializer(serializers.ModelSerializer):
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
                  'image1',
                  'image2',
                  'image3',
                  'image4',
                  'image5',
                  'image6',
                  'image7',
                  'image8',
                  'image9',
                  'image10',
                  'total_price',
                  'created_at',
                  'updated_at',]


class ApartmentBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ApartmentBooking
        fields = ['apartment_id',
                  'start_date',
                  'end_date']


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
