from django.db.models.functions import ExtractMonth, ExtractYear
from django.db.models import Count, Sum, F, ExpressionWrapper, FloatField
from rest_framework import generics
from rest_framework.views import APIView
from django.db.models import Count
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser
import cloudinary
import cloudinary.uploader
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from rest_framework.pagination import PageNumberPagination


from apartment import models, serializers
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .utils import PaystackAPI, UserService

user_service = UserService()
paystack_api = PaystackAPI()

# Create your views here.



class PageNumberPaginationMixin:
    pagination_class = PageNumberPagination
    page_size = 10 

class ListApartmentView(generics.CreateAPIView):
    """View for listing apartment on platform"""
    serializer_class = serializers.ListApartmentSerializer
    authentication_classes = [TokenAuthentication]
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        request_body=serializers.ListApartmentSerializer,
        operation_description="Create a new apartment with images."
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            token = request.headers.get('Authorization')
            clear_token = token[7:]

            if token is None:
                return Response({"status": False, "message": "unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception:
            return Response({"status": False, "message": "Cannot get Auth token"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = user_service.get_user(token=clear_token)
            verified_status = user['data']['isVerified']
            profile_type = user['data']['profile_type']
            isActiveHost = user['data']['isActiveHost']
            user_id = user['data']['id']
            user_name = user['data']['first_name'] + \
                " " + user['data']['last_name']
        except Exception:
            return Response({"status": False, "message": "User service error"}, status=status.HTTP_401_UNAUTHORIZED)
        if not verified_status:
            return Response({"status": False,  "message": "Your email is not verified. Please verify your email to continue."}, status=status.HTTP_401_UNAUTHORIZED)
        if not isActiveHost:
            return Response({"status": False,  "message": "Your profile is not yet verified as a host. Please wait for host verification to continue."}, status=status.HTTP_401_UNAUTHORIZED)
        if profile_type == 'Host' and isActiveHost == True:
            if serializer.is_valid():
                image_fields = ['image1', 'image2',
                                'image3', 'image4', 'image5']
                upload_results = []

                for field in image_fields:
                    image_file = request.data.get(field)
                    if image_file:
                        upload_result = cloudinary.uploader.upload(
                            image_file)
                        upload_results.append(upload_result['secure_url'])
                        serializer.validated_data[field] = upload_result['secure_url']

                if upload_results:
                    apartment = serializer.save()
                    apartment.owner_id = user_id
                    apartment.owner_name = user_name
                    apartment.is_draft = False
                    apartment.save()
                    return Response({"status": False,  "message": "Apartment added successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
                else:
                    return Response("At least one image is required.", status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status": False,  "message": "You are not authorized to make this request"}, status=status.HTTP_401_UNAUTHORIZED)


class SaveApartmentDraftView(generics.CreateAPIView):
    """View for listing apartment on platform"""
    serializer_class = serializers.SaveApartmentDraftSerializer
    authentication_classes = [TokenAuthentication]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            token = request.headers.get('Authorization')
            clear_token = token[7:]
            if token is None:
                return Response({"status": False, "message": "unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception:
            return Response({"status": False, "message": "Cannot get Auth token"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = user_service.get_user(token=clear_token)
            verified_status = user['data']['isVerified']
            profile_type = user['data']['profile_type']
            isActiveHost = user['data']['isActiveHost']
            user_id = user['data']['id']
            user_name = user['data']['first_name'] + \
                " " + user['data']['last_name']

        except Exception:
            return Response({"status": False, "message": "User service error"}, status=status.HTTP_401_UNAUTHORIZED)
        if not verified_status:
            return Response({"status": False,  "message": "Your email is not verified. Please verify your email to continue."}, status=status.HTTP_401_UNAUTHORIZED)
        if not isActiveHost:
            return Response({"status": False,  "message": "Your profile is not yet verified as a host. Please wait for host verification to continue."}, status=status.HTTP_401_UNAUTHORIZED)
        if profile_type == 'Host' and isActiveHost == True:
            if serializer.is_valid():
                apartment = serializer.save()
                for i in range(1, 6):
                    image_field_name = f"image{i}"
                    image_file = request.data.get(image_field_name)
                    if image_file:
                        upload_result = cloudinary.uploader.upload(
                            image_file)
                        setattr(apartment, image_field_name,
                                upload_result['secure_url'])

                apartment.is_draft = True
                apartment.owner_id = user_id
                apartment.owner_name = user_name
                apartment.save()
                return Response({"status": True, "message": "Draft saved successfully", "apartment_id": apartment.id}, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PublishDraftApartmentView(APIView):
    """View for listing apartments that are saved as draft on the platform"""
    serializer_class = serializers.UnlistApartmentSerializer
    authentication_classes = [TokenAuthentication]

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            token = request.headers.get('Authorization')
            clear_token = token[7:]
            if token is None:
                return Response({"status": False, "message": "unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception:
            return Response({"status": False, "message": "Cannot get Auth token"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = user_service.get_user(token=clear_token)
            user_id = user['data']['id']
            verified_status = user['data']['isVerified']
            profile_type = user['data']['profile_type']
        except Exception:
            return Response({"status": False, "message": "User service error"}, status=status.HTTP_401_UNAUTHORIZED)
        apartment_id = self.kwargs.get('id')
        apartment = models.Apartment.objects.get(
            id=apartment_id)
        if int(apartment.owner_id) == user_id:
            apartment.is_draft = False
            apartment.save()
            return Response({"status": True, "message": "Apartment is no longer a draft"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"status": False, "message": "You are not the owner of this property"}, status=status.HTTP_401_UNAUTHORIZED)


class UnlistApartmentView(APIView):
    """View for unlisting apartment from platform"""
    serializer_class = serializers.UnlistApartmentSerializer
    authentication_classes = [TokenAuthentication]

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            token = request.headers.get('Authorization')
            clear_token = token[7:]
            if token is None:
                return Response({"status": False, "message": "unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception:
            return Response({"status": False, "message": "Cannot get Auth token"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = user_service.get_user(token=clear_token)
            user_id = user['data']['id']
            verified_status = user['data']['isVerified']
            profile_type = user['data']['profile_type']
        except Exception:
            return Response({"status": False, "message": "User service error"}, status=status.HTTP_401_UNAUTHORIZED)
        apartment = models.Apartment.objects.get(
            id=serializer.data.get('id'))
        if apartment.owner_id == user_id:
            apartment.status = 'Unlisted'
            apartment.save()
        else:
            return Response({"status": False, "message": "You are not the owner of this property"}, status=status.HTTP_401_UNAUTHORIZED)


class EditApartmentView(APIView):
    """View for listing apartment on platform"""
    serializer_class = serializers.ListApartmentSerializer
    authentication_classes = [TokenAuthentication]
    parser_classes = (MultiPartParser, FormParser)

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            token = request.headers.get('Authorization')
            clear_token = token[7:]

            if token is None:
                return Response({"status": False, "message": "unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception:
            return Response({"status": False, "message": "Cannot get Auth token"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = user_service.get_user(token=clear_token)
            verified_status = user['data']['isVerified']
            profile_type = user['data']['profile_type']
            isActiveHost = user['data']['isActiveHost']
            user_id = user['data']['id']
            user_name = user['data']['first_name'] + \
                " " + user['data']['last_name']
        except Exception:
            return Response({"status": False, "message": "User service error"}, status=status.HTTP_401_UNAUTHORIZED)
        if not verified_status:
            return Response({"status": False,  "message": "Your email is not verified. Please verify your email to continue."}, status=status.HTTP_401_UNAUTHORIZED)
        if not isActiveHost:
            return Response({"status": False,  "message": "Your profile is not yet verified as a host. Please wait for host verification to continue."}, status=status.HTTP_401_UNAUTHORIZED)
        if profile_type == 'Host' and isActiveHost == True:
            apartment_id = self.kwargs.get('id')
            apartment = models.Apartment.objects.filter(
                id=apartment_id).first()
            if not apartment:
                return Response({"status": False, "message": "apartment not found"}, status=status.HTTP_404_NOT_FOUND)
            if int(apartment.owner_id) != user_id:
                return Response({"status": False, "message": "You cannot edit this apartment. it is not yours"}, status=status.HTTP_401_UNAUTHORIZED)

            if serializer.is_valid():
                apartment = serializer.save()
                for i in range(1, 6):
                    image_field_name = f"image{i}"
                    image_file = request.data.get(image_field_name)
                    if image_file:
                        upload_result = cloudinary.uploader.upload(
                            image_file)
                        setattr(apartment, image_field_name,
                                upload_result['secure_url'])

                apartment.is_draft = True
                apartment.owner_id = user_id
                apartment.owner_name = user_name
                apartment.save()
                return Response({"status": True, "message": "Apartment edited successfully"}, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteApartmentView(generics.DestroyAPIView):
    """View for deleting apartment from platform"""
    serializer_class = serializers.ApartmentSerializer
    authentication_classes = [TokenAuthentication]

    def delete(self, request, *args, **kwargs):
        try:
            token = request.headers.get('Authorization')
            clear_token = token[7:]
            if token is None:
                return Response({"status": False, "message": "unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception:
            return Response({"status": False, "message": "Cannot get Auth token"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = user_service.get_user(token=clear_token)
            user_id = user['data']['id']
        except Exception:
            return Response({"status": False, "message": "User service error"}, status=status.HTTP_401_UNAUTHORIZED)
        apartment_id = self.kwargs.get('id')
        apartment = models.Apartment.objects.filter(
            id=apartment_id).first()
        if not apartment:
            return Response({"status": False, "message": "apartment not found"}, status=status.HTTP_404_NOT_FOUND)
        if int(apartment.owner_id) != user_id:
            return Response({"status": False, "message": "You cannot delete this apartment. it is not yours"}, status=status.HTTP_401_UNAUTHORIZED)
        apartment.delete()

        return Response({"status": True, "message": f"apartment with id {apartment_id} has been deleted"})


class GetApartmentAmenitiesView(generics.ListAPIView):
    serializer_class = serializers.GetApartmentAmenitiesSerializer
    queryset = models.ApartmentAmenities.objects.all()
    pagination_class = None


class GetApartmentSafetyAndSecurityItemsView(generics.ListAPIView):
    serializer_class = serializers.GetSaftyAndSecuritySerializer
    queryset = models.SaftyAndSecurity.objects.all()
    pagination_class = None


class GetApartmentRulesView(generics.ListAPIView):
    serializer_class = serializers.GetApartmentRulesSerializer
    queryset = models.ApartmentRules.objects.all()
    pagination_class = None


class GetApartmentAdditionalChargesView(generics.ListAPIView):
    serializer_class = serializers.GetAdditionalChargesSerializer
    queryset = models.AdditionalCharge.objects.all()
    pagination_class = None


class GetApartmentCancellationPolicyView(generics.ListAPIView):
    serializer_class = serializers.GetCancellationPolicySerializer
    queryset = models.CancellationPolicy.objects.all()
    pagination_class = None


class CheckoutApartmentView(generics.ListAPIView):
    """View for user to book apartment"""
    serializer_class = serializers.CheckoutSerializer
    authentication_classes = [TokenAuthentication]
    pagination_class = None

    def get(self, request, *args, **kwargs):
        try:
            token = request.headers.get('Authorization')
            clear_token = token[7:]

            if token is None:
                return Response({"status": False, "message": "unauthenticated"})
        except Exception:
            return Response({"status": False, "message": "Cannot get Auth token"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = user_service.get_user(token=clear_token)
            user_id = user['data']['id']
            verified_status = user['data']['isVerified']
        except Exception:
            return Response({"status": False, "message": "User service error"}, status=status.HTTP_401_UNAUTHORIZED)
        if not verified_status:
            return Response({"status": False, "message": "Your email is not verified. Please verify your email to continue."}, status=status.HTTP_401_UNAUTHORIZED)

        reference = self.kwargs.get('reference')
        booking = models.ApartmentBooking.objects.filter(
            payment_reference=reference).first()
        apartment_id = booking.apartment_id.id
        apartment = models.Apartment.objects.filter(
            id=apartment_id).first()

        apartment_data = serializers.ApartmentSerializer(apartment)

        serializer = self.serializer_class(booking)
        return Response({"status": True, "message": "Booking retrieved successfully", "data": {"user details": serializer.data, "apartment details": apartment_data.data}}, status=status.HTTP_200_OK)


class BookApartmentView(generics.CreateAPIView):
    """View for user to book apartment"""
    serializer_class = serializers.ApartmentBookingSerializer
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            try:
                token = request.headers.get('Authorization')
                clear_token = token[7:]
                if token is None:
                    return Response({"status": False, "message": "unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
            except Exception:
                return Response({"status": False, "message": "Cannot get Auth token"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = user_service.get_user(token=clear_token)
                user_id = user['data']['id']
                verified_status = user['data']['isVerified']
            except Exception:
                return Response({"status": False, "message": "User service error"}, status=status.HTTP_401_UNAUTHORIZED)

            if not verified_status:
                return Response({"status": False,  "message": "Your email is not verified. Please verify your email to continue."}, status=status.HTTP_401_UNAUTHORIZED)

            apartment = models.Apartment.objects.get(
                id=serializer.data['apartment_id'])
            user_email = user['data']['email']
            if apartment.isOccupied:
                return Response({"status": False, "message": "This apartment is full"})


            # this is a check for if master bedroom is available
            if request.data['paid_for_master_bedroom'] == True:
                if apartment.is_master_bedroom_available == False:
                    return Response({"status": False, "message": "This apartments master bedroom is taken."})


            booking_start_date = request.data['start_date']
            booking_end_date = request.data['end_date']

            if request.data['end_date'] < request.data['start_date']:
                return Response({"status": False, "message": "Start date cannot be greater than end date"})

            paystack_response = paystack_api.initialise_transaction(
                email=user_email, amount=apartment.total_price)
            authorization_url = paystack_response['data']['authorization_url']
            reference = paystack_response['data']['reference']

            booking = models.ApartmentBooking.objects.create(
                apartment_id=apartment,
                user_id=user_id,
                amount_paid=apartment.total_price,
                start_date=request.data['start_date'],
                end_date=request.data['end_date'],
                paid_for_master_bedroom=request.data['paid_for_master_bedroom'],
                payment_reference=reference,
                payment_link=authorization_url,
                email=user_email,
                first_name=user['data']['first_name'],
                last_name=user['data']['last_name'],
                phone_number=user['data']['phone_number'],
                no_of_guests=request.data['no_of_guests'],
                cover_photo=apartment.image1
            )

            send_apartment_booking_email(
                user_email, apartment.address, booking_start_date, booking_end_date)

            trnx_details = models.Transaction.objects.create(
                user_id=user_id,
                amount=apartment.total_price,
                payment_reference=reference,
                transaction_status="pending",
                description="Apartment Boooking",
                recipient="99Apartment",
                payment_method="PayStack",
            )
            return Response({"status": True, "message": "Apartment booked successfully", "data": {"reference": reference}}, status=status.HTTP_201_CREATED)


class VerifyApartmentBooking(APIView):
    """View for verifying apartment booking payment"""

    def get(self, request, *args, **kwargs):
        payment_reference = self.kwargs.get('reference')

        paystack_payment_verification_status = paystack_api.verify_transaction(
            reference=payment_reference)
        if paystack_payment_verification_status['data']['status'] == 'success':
            apartment_booking = models.ApartmentBooking.objects.filter(
                payment_reference=payment_reference).first()
            apartment_id = apartment_booking.apartment_id.id
            if apartment_booking.isPaidFor == True:
                return Response({"status": False, "message": "This payment has been verified already."})
            apartment_booking.isPaidFor = True
            apartment_booking.save()
            apartment = models.Apartment.objects.filter(
                id=apartment_id).first()
            apartment.number_of_occupants += 1
            apartment.save()
            trnx_details = models.Transaction.objects.filter(
                payment_reference=payment_reference).first()
            trnx_details.transaction_status = "success"
            trnx_details.save()

            # email builder
            start_date = apartment_booking.start_date
            end_date = apartment_booking.end_date
            user_email = apartment_booking.email
            address = apartment_booking.apartment_id.address
            apartment_name = apartment_booking.apartment_id.name

            send_apartment_payment_successful_email(user_email, address, apartment_name, start_date, end_date)
            return Response({"status": True, "message": "Payment verified successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": False, "message": "Payment not verified"}, status=status.HTTP_400_BAD_REQUEST)


class SearchApartmentView(generics.ListAPIView):
    """View for searching for apartments"""
    serializer_class = serializers.ApartmentSerializer
    queryset = models.Apartment.objects.filter(isOccupied=False)

    def get(self, request, *args, **kwargs):
        city = request.query_params.get('city', None)
        no_of_rooms = request.query_params.get('no_of_rooms', None)
        try:
            if city:
                items = models.Apartment.objects.filter(city=city)
            if no_of_rooms:
                items = models.Apartment.objects.filter(
                    number_of_rooms=no_of_rooms)
            serializer = serializers.ResponseSerializer({"data": items})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response({"status": False, "message": "server error"}, status=status.HTTP_400_BAD_REQUEST)


class PaginatedListApartmentView(generics.ListAPIView):
    """View for listing all apartments"""
    serializer_class = serializers.ApartmentSerializer
    queryset = models.Apartment.objects.filter(
        isOccupied=False, status='Listed')

    def get(self, request, *args, **kwargs):
        city = request.query_params.get('city', None)
        no_of_rooms = request.query_params.get('no_of_rooms', None)
        air_conditioning = request.query_params.get('air_conditioning', None)
        kitchen = request.query_params.get('kitchen', None)
        washer = request.query_params.get('washer', None)
        work_space = request.query_params.get('work_space', None)
        smoke_alarm = request.query_params.get('smoke_alarm', None)
        pool = request.query_params.get('pool', None)
        indoor_fireplace = request.query_params.get('indoor_fireplace', None)
        ev_charger = request.query_params.get('ev_charger', None)
        hot_tub = request.query_params.get('hot_tub', None)
        free_parking = request.query_params.get('free_parking', None)

        allows_pets = request.query_params.get('allows_pets', None)
        allows_party = request.query_params.get('allows_party', None)
        allows_smoking = request.query_params.get('allows_smoking', None)

        has_tenant = request.query_params.get('has_tenant', None)
        vacant = request.query_params.get('vacant', None)

        try:
            if city:
                items = models.Apartment.objects.filter(city=city)
            if no_of_rooms:
                items = models.Apartment.objects.filter(
                    number_of_rooms=no_of_rooms)
            if air_conditioning:
                items = models.Apartment.objects.filter(
                    amenities__contains=['air conditioning'])

            if kitchen:
                items = models.Apartment.objects.filter(
                    amenities__contains=['kitchen'])

            if washer:
                items = models.Apartment.objects.filter(
                    amenities__contains=['washer'])

            if work_space:
                items = models.Apartment.objects.filter(
                    amenities__contains=['work space'])

            if smoke_alarm:
                items = models.Apartment.objects.filter(
                    amenities__contains=['smoke alarm'])

            if pool:
                items = models.Apartment.objects.filter(
                    amenities__contains=['pool'])

            if indoor_fireplace:
                items = models.Apartment.objects.filter(
                    amenities__contains=['indoor fireplace'])

            if ev_charger:
                items = models.Apartment.objects.filter(
                    amenities__contains=['ev charger'])

            if hot_tub:
                items = models.Apartment.objects.filter(
                    amenities__contains=['hot tub'])

            if free_parking:
                items = models.Apartment.objects.filter(
                    amenities__contains=['free parking'])

            if allows_pets:
                items = models.Apartment.objects.exclude(
                    amenities__contains=['no pets'])

            if allows_party:
                items = models.Apartment.objects.exclude(
                    rules__contains=['no parties'])

            if allows_smoking:
                items = models.Apartment.objects.exclude(
                    rules__contains=['no smoking'])

            if has_tenant:
                items = models.Apartment.objects.filter(
                    hasOccupants=True, isOccupied=False)

            if vacant:
                items = models.Apartment.objects.filter(hasOccupants=False)

            serializer = serializers.ResponseSerializer({"data": items})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = serializers.ResponseSerializer({"data": queryset})
            return Response(serializer.data, status=status.HTTP_200_OK)


class HostApartmentListView(generics.ListAPIView):
    """This view is for showing all the hosts apartments"""
    serializer_class = serializers.HostApartmentSerializer
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        try:
            token = request.headers.get('Authorization')
            clear_token = token[7:]
            if token is None:
                return Response({"status": False, "message": "unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception:
            return Response({"status": False, "message": "Cannot get Auth token"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = user_service.get_user(token=clear_token)
            user_id = user['data']['id']
            verified_status = user['data']['isVerified']
        except Exception:
            return Response({"status": False, "message": "User service error"}, status=status.HTTP_401_UNAUTHORIZED)
        apartments = models.Apartment.objects.filter(
            owner_id=user_id)

        qs = self.serializer_class(apartments, many=True)
        annotated_apartments = apartments.annotate(
            maintenance_count=Count('maintenance'), occupancy_rate=ExpressionWrapper(
                F('number_of_occupants') * 100 / (F('number_of_rooms') + 1),
                output_field=FloatField()
            ), amount_generated=Sum('apartmentbooking__amount_paid')
        )
        qs = self.serializer_class(annotated_apartments, many=True)

        return Response({"status": True, "message": "Data retrieved successfully", "count": len(qs.data), "data": qs.data}, status=status.HTTP_200_OK)


class HostApartmentByIdView(generics.RetrieveAPIView):
    """View for getting the details of one host apartment"""
    serializer_class = serializers.ApartmentSerializer
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        try:
            token = request.headers.get('Authorization')
            clear_token = token[7:]
            if token is None:
                return Response({"status": False, "message": "unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception:
            return Response({"status": False, "message": "Cannot get Auth token again"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = user_service.get_user(token=clear_token)
            user_id = user['data']['id']
            verified_status = user['data']['isVerified']
        except Exception:
            return Response({"status": False, "message": "User service error"}, status=status.HTTP_401_UNAUTHORIZED)

        apartment_id = self.kwargs.get('id')
        apartment = models.Apartment.objects.filter(id=apartment_id).first()
        if apartment:
            serializer = self.serializer_class(apartment)
            if int(apartment.owner_id) == user_id:
                return Response({"status": True, "message": "Apartment retrieved successfully", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": False, "message": "You are not the owner of this apartment"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status": False, "message": "Apartment not found"}, status=status.HTTP_400_BAD_REQUEST)


class HostApartmentMaintenanceListView(generics.ListAPIView):
    """This view is for showing all the hosts apartments maintenance details"""
    serializer_class = serializers.HostMaintenanceSerializer
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        try:
            token = request.headers.get('Authorization')
            clear_token = token[7:]
            if token is None:
                return Response({"status": False, "message": "unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception:
            return Response({"status": False, "message": "Cannot get Auth token"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = user_service.get_user(token=clear_token)
            user_id = user['data']['id']
        except Exception:
            return Response({"status": False, "message": "User service error"}, status=status.HTTP_401_UNAUTHORIZED)
        queryset = models.Maintenance.objects.filter(
            apartment_id__owner_id=user_id)
        qs = self.serializer_class(queryset, many=True)

        return Response({"status": True, "message": "Data retrieved successfully", "count": len(qs.data), "data": qs.data}, status=status.HTTP_200_OK)


class ApartmentDetailView(generics.RetrieveAPIView):
    """View for getting the details of one apartment"""
    serializer_class = serializers.ApartmentSerializer

    def get(self, request, *args, **kwargs):
        try:
            apartment_id = self.kwargs.get('id')
            apartment = models.Apartment.objects.filter(
                id=apartment_id).first()
            if apartment:
                if apartment.status == 'Unlisted':
                    return Response({"status": False, "message": "This apartment is not yet listed"}, status=status.HTTP_400_BAD_REQUEST)
                serializer = self.serializer_class(apartment)
                return Response({"status": True, "message": "Apartment retrieved successfully", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": False, "message": "Apartment not found"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"status": False, "message": "server error"}, status=status.HTTP_400_BAD_REQUEST)


class BookApartmentInspectionView(generics.CreateAPIView):
    """View for booking apartment inspection"""
    serializer_class = serializers.BookApartmentInsectionSerializer
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            token = request.headers.get('Authorization')
            clear_token = token[7:]
            if token is None:
                raise AuthenticationFailed("unauthenticated")
            try:
                user = user_service.get_user(token=clear_token)
                user_id = user['data']['id']
                verified_status = user['data']['isVerified']
            except Exception:
                return Response({"status": False, "message": "User service error"}, status=status.HTTP_401_UNAUTHORIZED)
            if not verified_status:
                return Response({"status": False,  "message": "Your email is not verified. Please verify your email to continue."}, status=status.HTTP_401_UNAUTHORIZED)

            user_email = user['data']['email']
            apartment = models.Apartment.objects.get(
                id=serializer.data['apartment_id'])
            address = apartment.address
            inspection = models.ApartmentInspection.objects.create(
                apartment_id=apartment,
                user_id=user_id,
                inspection_date=request.data['inspection_date'],
                inspection_time=request.data['inspection_time'],
            )
            # try:
            #     send_apartment_inspection_email(
            #         user_email, address, inspection_date=request.data['inspection_date'])
            # except Exception:
            #     return Response({"status": False, "message": "Server Error"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"status": True, "message": "Inspection booked successfully"}, status=status.HTTP_200_OK)


class GetApartmentInspectionView(generics.ListAPIView):
    """View for listing all apartment inspections"""
    serializer_class = serializers.ApartmentInsectionSerializer
    queryset = models.ApartmentInspection.objects.filter(isInspected=False)

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = serializers.ApartmentInsectionResponseSerializer({
                                                                      "data": queryset})
        return Response(serializer.data)


def send_apartment_inspection_email(user_email, address, inspection_date):
    subject = 'Apartment Inspection.'
    from_email = settings.EMAIL_HOST_USER

    email_template = render_to_string(
        'inspection/emails/apartment-inspection-booking-complete.html', {'email': user_email, 'address': address, 'inspection_date': inspection_date})
    email_verification_email = EmailMessage(
        subject, email_template, from_email, [user_email]
    )
    email_verification_email.fail_silently = True
    email_verification_email.send()


def send_apartment_booking_email(user_email, address, start_date, end_date):
    subject = 'Apartment Booking.'
    from_email = settings.EMAIL_HOST_USER

    email_template = render_to_string(
        'inspection/emails/apartment-booking-complete.html', {'email': user_email, 'address': address, 'start_date': start_date, 'end_date': end_date})
    email_verification_email = EmailMessage(
        subject, email_template, from_email, [user_email]
    )
    email_verification_email.fail_silently = True
    email_verification_email.send()

def send_apartment_payment_successful_email(user_email, address, apartment_name, start_date, end_date):
    subject = 'Payment Successful.'
    from_email = settings.EMAIL_HOST_USER

    email_template = render_to_string(
        'inspection/emails/apartment-payment-successful.html', {'email': user_email, 'apartment_name': apartment_name, 'address': address, 'start_date': start_date, 'end_date': end_date})
    email_verification_email = EmailMessage(
        subject, email_template, from_email, [user_email]
    )
    email_verification_email.fail_silently = True
    email_verification_email.send()

class ApartmentReviewsListView(generics.ListAPIView):
    """View for getting an apartments reviews"""
    serializer_class = serializers.GetApartmentReviewsSerializer
    pagination_class = None

    # queryset = models.ApartmentReview.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            apartment_id = self.kwargs.get('apartment_id')
            reviews = models.ApartmentReview.objects.filter(
                apartment_id_id=apartment_id)
            reviewed_apartment = models.Apartment.objects.filter(
                id=apartment_id).first()
            number_of_reviews = reviewed_apartment.number_of_reviews

            serializer = self.serializer_class(reviews, many=True)
            return Response({"status": True, "message": "Data retrieved successfully", "number_of_reviews": number_of_reviews, "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"status": False, "message": "server error"}, status=status.HTTP_400_BAD_REQUEST)


class ReviewApartmentView(generics.CreateAPIView):
    """View for reviewing an apartment"""
    serializer_class = serializers.ApartmentReviewSerializer
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            try:
                token = request.headers.get('Authorization')
                clear_token = token[7:]
                if token is None:
                    raise AuthenticationFailed("unauthenticated")
            except Exception:
                return Response({"status": False, "message": "Cannot get Auth token"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                user = user_service.get_user(token=clear_token)
                user_id = user['data']['id']
            except Exception:
                return Response({"status": False, "message": "User service error"}, status=status.HTTP_401_UNAUTHORIZED)
            review = serializer.data.get('review')
            rating = serializer.data.get('rating')
            if float(rating) > 5:
                return Response({"status": False, "message": "you cannot give a rating of more than 5"})
            apartment_id = serializer.data.get('apartment_id')
            apartment = models.Apartment.objects.filter(
                id=apartment_id).first()

            review = models.ApartmentReview.objects.create(apartment_id=apartment,
                                                           user_id=user_id,
                                                           review=review,
                                                           rating=rating)
            number_of_reviews = models.ApartmentReview.objects.count()
            apartment.number_of_reviews = number_of_reviews
            rating_list = []
            number_of_ratings = models.ApartmentReview.objects.all().values()
            for i in number_of_ratings:
                rating_list.append(i['rating'])
            apartment_rating = sum(rating_list) / len(rating_list)
            apartment.rating = apartment_rating
            apartment.save()
            return Response({"status": True, "message": "Apartment reviewed successfully"}, status=status.HTTP_200_OK)


class GetApartmentCitiesView(generics.ListAPIView):
    """View for getting an apartments locations"""
    serializer_class = serializers.ApartmentCitiesSerializer
    pagination_class = None

    def get(self, request, *args, **kwargs):
        apartment_cities = models.Apartment.objects.all().values()
        cities = []
        for i in apartment_cities:
            cities.append(i['city'])
        return Response({"status": True, "message": "Data retrieved successfully", "data": {"number_of_cities": len(cities), "cities": cities}}, status=status.HTTP_200_OK)


class MaintenanceRequestView(generics.CreateAPIView):
    serializer_class = serializers.MaintenanceRequestSerializer
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            try:
                token = request.headers.get('Authorization')
                clear_token = token[7:]
                if token is None:
                    raise AuthenticationFailed("unauthenticated")
            except Exception:
                return Response({"status": False, "message": "Cannot get Auth token"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                user = user_service.get_user(token=clear_token)
                user_id = user['data']['id']
                user_email = user['data']['email']
                verified_status = user['data']['isVerified']
                user_full_name = user['data']['first_name'] + " " + user['data']['last_name']
            except Exception:
                return Response({"status": False, "message": "User service error"}, status=status.HTTP_401_UNAUTHORIZED)
            if not verified_status:
                return Response({"status": False,  "message": "Your email is not verified. Please verify your email to continue."}, status=status.HTTP_401_UNAUTHORIZED)

            apartment = get_user_current_apartment(user_id)
            maintenance_request = models.Maintenance.objects.create(
                apartment_id=apartment,
                user_id=user_id,
                name=user_full_name,
                phone_number=user['data']['phone_number'],
                maintenance_category=serializer.data.get(
                    'maintenance_category'),
                maintenance_type=serializer.data.get('maintenance_type'),
                description=serializer.data.get('description')
            )

            send_maintenance_request_email(user_email, apartment.address)
            return Response({"status": True, "message": "Maintenance request sent successfully."}, status=status.HTTP_200_OK)


def send_maintenance_request_email(user_email, address):
    subject = 'Apartment Maintenance Request.'
    from_email = settings.EMAIL_HOST_USER

    email_template = render_to_string(
        'inspection/emails/apartment-maintenance-request-complete.html', {'email': user_email, 'address': address})
    email_verification_email = EmailMessage(
        subject, email_template, from_email, [user_email]
    )
    email_verification_email.fail_silently = True
    email_verification_email.send()


def get_user_current_apartment(user_id):
    apartment = models.ApartmentBooking.objects.filter(user_id=user_id).last()
    return apartment.apartment_id

class GetUserCurrentApartmentView(APIView):
    serializer_class = serializers.ApartmentSerializer

    def get(self, request):
        apartment = models.ApartmentBooking.objects.filter(user_id=user_id).last()
        qs = self.serializer_class(apartment)
        return Response({'status': True, 'message': 'User apartment details retrieved successfully', 'data':qs.data}, status=status.HTTP_200_OK)
        


class UserMaintenanceHistoryView(generics.ListAPIView):
    serializer_class = serializers.MaintenanceSerializer
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        try:
            token = request.headers.get('Authorization')
            clear_token = token[7:]
            if token is None:
                raise AuthenticationFailed("unauthenticated")
        except Exception:
            return Response({"status": False, "message": "Cannot get Auth token"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = user_service.get_user(token=clear_token)
            print("user", user)
            user_id = user['data']['id']
            verified_status = user['data']['isVerified']
        except Exception:
            return Response({"status": False, "message": "User service error"}, status=status.HTTP_401_UNAUTHORIZED)
        if not verified_status:
            return Response({"status": False,  "message": "Your email is not verified. Please verify your email to continue."}, status=status.HTTP_401_UNAUTHORIZED)

        queryset = models.Maintenance.objects.filter(user_id=user_id)
        qs = self.serializer_class(queryset, many=True)
        return Response({"status": True, "message": "Data retrieved successfully", "data": qs.data}, status=status.HTTP_200_OK)


class TransactionDetailsView(generics.RetrieveAPIView):
    serializer_class = serializers.TransactionSerializer
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        try:
            token = request.headers.get('Authorization')
            clear_token = token[7:]
            if token is None:
                raise AuthenticationFailed("unauthenticated")
        except Exception:
            return Response({"status": False, "message": "Cannot get Auth token"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = user_service.get_user(token=clear_token)
            user_id = user['data']['id']
            verified_status = user['data']['isVerified']
        except Exception:
            return Response({"status": False, "message": "User service error"}, status=status.HTTP_401_UNAUTHORIZED)
        if not verified_status:
            return Response({"status": False,  "message": "Your email is not verified. Please verify your email to continue."}, status=status.HTTP_401_UNAUTHORIZED)

        trnx_id = self.kwargs.get('id')
        queryset = models.Transaction.objects.filter(id=trnx_id).first()
        qs = self.serializer_class(queryset)
        return Response({"status": True, "message": "Data retrieved successfully", "data": qs.data}, status=status.HTTP_200_OK)


class TransactionHistoryView(generics.ListAPIView):
    serializer_class = serializers.TransactionSerializer
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        try:
            token = request.headers.get('Authorization')
            clear_token = token[7:]
            if token is None:
                raise AuthenticationFailed("unauthenticated")
        except Exception:
            return Response({"status": False, "message": "Cannot get Auth token"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = user_service.get_user(token=clear_token)
            user_id = user['data']['id']
            verified_status = user['data']['isVerified']
        except Exception:
            return Response({"status": False, "message": "Cannot get Auth token"}, status=status.HTTP_400_BAD_REQUEST)
        if not verified_status:
            return Response({"status": False,  "message": "Your email is not verified. Please verify your email to continue."}, status=status.HTTP_401_UNAUTHORIZED)
        queryset = models.Transaction.objects.filter(user_id=user_id)
        qs = self.serializer_class(queryset, many=True)
        return Response({"status": True, "message": "Data retrieved successfully", "data": qs.data}, status=status.HTTP_200_OK)


class HostAnalyticsView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        try:
            token = request.headers.get('Authorization')
            clear_token = token[7:]
            if token is None:
                return Response({"status": False, "message": "unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception:
            return Response({"status": False, "message": "Cannot get Auth token"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = user_service.get_user(token=clear_token)
            user_id = user['data']['id']
            verified_status = user['data']['isVerified']
        except Exception:
            return Response({"status": False, "message": "User service error"}, status=status.HTTP_401_UNAUTHORIZED)
        maintenance_queryset = models.Maintenance.objects.filter(
            apartment_id__owner_id=user_id)
        maintenance_qs = serializers.MaintenanceSerializer(
            maintenance_queryset, many=True)

        service_queryset = models.Service.objects.filter(
            apartment_id__owner_id=user_id)

        service_qs = serializers.ServiceSerializer(
            service_queryset, many=True)

        apartments = models.Apartment.objects.filter(owner_id=user_id)

        total_occupants = apartments.aggregate(total_occupants=Sum('number_of_occupants'))[
            'total_occupants'] or 0

        total_revenue = apartments.aggregate(total_revenue=Sum('apartmentbooking__amount_paid'))[
            'total_revenue'] or 0

        total_service_amount = service_queryset.aggregate(total_amount=Sum('amount'))[
            'total_amount'] or 0

        analytics_data = {"maintenance_count": len(maintenance_qs.data),
                          "service_count": len(service_qs.data),
                          "total_occupants": total_occupants,
                          "total_revenue": total_revenue,
                          "total_profit": total_revenue - total_service_amount,
                          "total_service_amount": total_service_amount,
                          "total_apartments": len(apartments)}

        return Response({"status": True, "message": "Data retrieved successfully", "data": analytics_data}, status=status.HTTP_200_OK)


class HostAnalyticsDummyView(APIView):
    def get(self, request):
        return Response({"status": True, "message": "Data retrieved successfully", "data": {"revenue": {
            "january": 4000,
            "february": 2000,
            "march": 6000,
            "april": 4000,
            "may": 10000,
            "june": 14000,
            "july": 3000,
            "august": 9000,
            "september": 7000,
            "october": 7500,
            "november": 6900,
            "december": 8000
        },
            "maintenance": {
            "january": 4000,
            "february": 2000,
            "march": 6000,
            "april": 4000,
            "may": 10000,
            "june": 14000,
            "july": 3000,
            "august": 9000,
            "september": 7000,
            "october": 7500,
            "november": 6900,
            "december": 8000
        }}})


class GetAllServicesView(generics.ListAPIView):
    """This view is for showing all the hosts apartments"""
    serializer_class = serializers.ServiceSerializer
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        try:
            token = request.headers.get('Authorization')
            clear_token = token[7:]
            if token is None:
                return Response({"status": False, "message": "unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception:
            return Response({"status": False, "message": "Cannot get Auth token"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = user_service.get_user(token=clear_token)
            user_id = user['data']['id']
            verified_status = user['data']['isVerified']
        except Exception:
            return Response({"status": False, "message": "User service error"}, status=status.HTTP_401_UNAUTHORIZED)
        services = models.Service.objects.filter(
            apartment_id__owner_id=user_id)

        total_amount = services.aggregate(total_amount=Sum('amount'))[
            'total_amount'] or 0
        qs = self.serializer_class(services, many=True)
        return Response({"status": True, "message": "Data retrieved successfully", "count": len(qs.data), "total_amount": total_amount, "data": qs.data}, status=status.HTTP_200_OK)


class ChangeApartmentView(APIView):
    serializer_class = serializers.ChangeApartmentSerializer
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            token = request.headers.get('Authorization')
            clear_token = token[7:]
            if token is None:
                return Response({"status": False, "message": "unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception:
            return Response({"status": False, "message": "Cannot get Auth token again"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = user_service.get_user(token=clear_token)
            user_id = user['data']['id']
            verified_status = user['data']['isVerified']
        except Exception:
            return Response({"status": False, "message": "User service error"}, status=status.HTTP_401_UNAUTHORIZED)

        if serializer.is_valid():
            apartment_change = serializer.save()
            apartment_change.resident_name = user['data']['first_name'] + " " + user['data']['last_name']
            apartment_change.email = user['data']['email']
            apartment_change.phone_number = user['data']['phone_number']
            apartment_change.save()

            apartment_change_notification = models.ChangeApartmentNotification.objects.create(resident_name=apartment_change.resident_name, message="This user wants to change apartments.")
            return Response({"status": True, "message": "Request submitted successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
