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
                  'hasOccupants',
                  'isOccupied',
                  'price',
                  'apartment_fees',
                  'amenities',
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
                  'user_id',
                  'start_date',
                  'end_date']


class ResponseSerializer(serializers.Serializer):
    status = serializers.BooleanField(default=True)
    message = serializers.CharField(default='Data retrieved successfully')
    data = ApartmentSerializer(many=True)


class ApartmentInsectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ApartmentInspection
        fields = ['apartment_id',
                  'user_id',
                  'inspection_date',
                  'isInspected',
                  'created_at',
                  'updated_at',]


class BookApartmentInsectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ApartmentInspection
        fields = ['apartment_id',
                  'user_id',
                  'inspection_date',
                  ]


class ApartmentInsectionResponseSerializer(serializers.Serializer):
    status = serializers.BooleanField(default=True)
    message = serializers.CharField(default='Data retrieved successfully')
    data = ApartmentInsectionSerializer(many=True)
