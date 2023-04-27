from rest_framework import generics
from drf_spectacular.utils import extend_schema

from rest_framework.response import Response
from apartment import models, serializers

import json

# Create your views here.

class ListApartmentView(generics.CreateAPIView):
    """View for listing apartment on platform"""
    pass

@extend_schema(methods=['PATCH'], exclude=True)
class UnlistApartmentView(generics.UpdateAPIView):
    """View for unlisting apartment from platform"""
    pass

class BookApartmentView(generics.CreateAPIView):
    """View for user to book apartment"""
    serializer_class = serializers.ApartmentSerializer

    def post(self, request):


@extend_schema(methods=['PATCH'], exclude=True)
class EditApartmentView(generics.UpdateAPIView):
    """View for editing apartment listing"""
    pass


class PaginatedListApartmentView(generics.ListAPIView):
    """View for listing all apartments"""
    serializer_class = serializers.ApartmentSerializer
    queryset = models.Apartment.objects.filter(isOccupied=False)

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = serializers.ResponseSerializer({"data": queryset})
        return Response(serializer.data)

class ApartmentDetailView(generics.RetrieveAPIView):
    """View for getting the details of one apartment"""
    serializer_class = serializers.ApartmentSerializer

    def get(self, request, *args, **kwargs):
        queryset = models.Apartment.objects.filter(id=self.kwargs.get('id'))
        serializer = serializers.ResponseSerializer({"data": queryset})

        return Response(serializer.data)


class BookApartmentInspectionView(generics.CreateAPIView):
    """View for booking apartment inspection"""
    serializer_class = serializers.ApartmentInsectionSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            try:
                apartment = models.Apartment.objects.get(id=serializer.data['apartment_id'])
                inspection = models.ApartmentInspection.objects.create(
                    apartment_id = apartment,
                    user_id = request.data['user_id'],
                    inspection_date = request.data['inspection_date'],
                )
            except Exception:
                return Response({'status':False,
                        'message':'Server error'})
            list_inspection = json.dumps(inspection)
            return Response({"message":"success", "data":list_inspection})

class GetApartmentInspectionView(generics.ListAPIView):
    """View for listing all apartment inspections"""
    serializer_class = serializers.ApartmentInsectionSerializer
    queryset = models.ApartmentInspection.objects.filter(isInspected=False)

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = serializers.ApartmentInsectionResponseSerializer({"data": queryset})
        return Response(serializer.data)