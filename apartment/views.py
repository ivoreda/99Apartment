from rest_framework import generics
from drf_spectacular.utils import extend_schema

from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from apartment import models, serializers

from .utils import PaystackAPI, UserService

import json

user_service = UserService()

paystack_api = PaystackAPI()

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
    serializer_class = serializers.ApartmentBookingSerializer
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            try:
                apartment = models.Apartment.objects.get(id=serializer.data['apartment_id'])
                if apartment.isOccupied:
                    return Response({"error": False, "message":"This apartment is full"})

                # get user
                token = request.headers.get('Authorization')
                user = user_service.get_user(token=token)
                user_id = user['data']['id']
                user_email = user['data']['email']
                price = apartment.price
                # get user email
                # get apartment price by id from the apartment model
                # send the amount and the user email to paystack endpoint
                # save reference and add authorization url to response
                paystack_response = paystack_api.initialise_transaction(email=user_email, amount=price)
                print("paystack response", paystack_response)
                authorization_url = paystack_response['data']['authorization_url']
                reference = paystack_response['data']['reference']

                booking = models.ApartmentBooking.objects.create(
                    apartment_id = apartment,
                    user_id = user_id,
                    start_date = request.data['start_date'],
                    end_date = request.data['end_date'],
                    payment_reference = reference
                )
                return Response({"message":"Apartment booked successfully", "data": {"authorization_url":authorization_url}}, status=status.HTTP_201_CREATED)
            except Exception:
                return Response({"error": True, "message":"server error"}, status=status.HTTP_400_BAD_REQUEST)





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
    serializer_class = serializers.BookApartmentInsectionSerializer
    authentication_classes = [TokenAuthentication]


    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            token = request.headers.get('Authorization')
            user = user_service.get_user(token=token)
            user_id = user['data']['id']
            apartment = models.Apartment.objects.get(id=serializer.data['apartment_id'])
            inspection = models.ApartmentInspection.objects.create(
                apartment_id = apartment,
                user_id = user_id,
                inspection_date = request.data['inspection_date'],
            )
            return Response({"status":True, "message":"Inspection booked successfully"})

class GetApartmentInspectionView(generics.ListAPIView):
    """View for listing all apartment inspections"""
    serializer_class = serializers.ApartmentInsectionSerializer
    queryset = models.ApartmentInspection.objects.filter(isInspected=False)

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = serializers.ApartmentInsectionResponseSerializer({"data": queryset})
        return Response(serializer.data)