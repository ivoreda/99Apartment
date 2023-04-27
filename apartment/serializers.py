from rest_framework import serializers
from . import models


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
                  'created_at',
                  'updated_at',]


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

class ApartmentInsectionResponseSerializer(serializers.Serializer):
    status = serializers.BooleanField(default=True)
    message = serializers.CharField(default='Data retrieved successfully')
    data = ApartmentInsectionSerializer(many=True)