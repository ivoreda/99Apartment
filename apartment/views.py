from rest_framework import generics
from rest_framework.views import APIView

from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed, ValidationError

from rest_framework import status
from apartment import models, serializers

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


from .utils import PaystackAPI, UserService

import json

user_service = UserService()

paystack_api = PaystackAPI()

# Create your views here.


class ListApartmentView(generics.CreateAPIView):
    """View for listing apartment on platform"""
    serializer_class = serializers.ListApartmentSerializer
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            token = request.headers.get('Authorization')
            if token is None:
                return Response({"status": False, "message": "unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
            try:
                user = user_service.get_user(token=token)
                user_id = user['data']['id']
                user_name = user['data']['first_name'] + \
                    " " + user['data']['last_name']
                verified_status = user['data']['isVerified']
                profile_type = user['data']['profile_type']

            except Exception:
                return Response({"status": False, "message": "unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
            if not verified_status:
                return Response({"status": False,  "message": "Your email is not verified. Please verify your email to continue."}, status=status.HTTP_401_UNAUTHORIZED)
            if profile_type == 'Landlord':
                apartment = models.Apartment.objects.create(
                    owner_id=user_id,
                    owner_name=user_name,

                )
            else:
                return Response({"status": False, "message": "You cannot list apartment because you are not a Landlord"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception:
            return Response({"status": False, "message": "server error"}, status=status.HTTP_400_BAD_REQUEST)


class UnlistApartmentView(generics.UpdateAPIView):
    """View for unlisting apartment from platform"""
    serializer_class = serializers.UnlistApartmentSerializer
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            token = request.headers.get('Authorization')
            if token is None:
                return Response({"status": False, "message": "unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
            try:
                user = user_service.get_user(token=token)
                user_id = user['data']['id']
                verified_status = user['data']['isVerified']
                profile_type = user['data']['profile_type']
            except Exception:
                return Response({"status": False, "message": "unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
            apartment = models.Apartment.objects.get(
                id=serializer.data.get('id'))
            if apartment.owner_id == user_id:
                apartment.status = 'Unlisted'
                apartment.save()
            else:
                return Response({"status": False, "message": "You are not the owner of this property"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception:
            return Response({"status": False, "message": "server error"}, status=status.HTTP_400_BAD_REQUEST)


class CheckoutApartmentView(generics.ListAPIView):
    """View for user to book apartment"""
    serializer_class = serializers.CheckoutSerializer
    authentication_classes = [TokenAuthentication]
    pagination_class = None

    def get(self, request, *args, **kwargs):
        try:
            token = request.headers.get('Authorization')
            if token is None:
                return Response({"status": False, "message": "unauthenticated"})
            try:
                user = user_service.get_user(token=token)
                user_id = user['data']['id']
                verified_status = user['data']['isVerified']
            except Exception:
                return Response({"status": False, "message": "unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
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
        except Exception:
            return Response({"status": False, "message": "server error"}, status=status.HTTP_400_BAD_REQUEST)


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
                print(token)
                if token is None:
                    return Response({"status": False, "message": "unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
                try:
                    user = user_service.get_user(token=token)
                    print(user)
                    user_id = user['data']['id']
                    verified_status = user['data']['isVerified']
                except Exception:
                    return Response({"status": False, "message": "unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
                if not verified_status:
                    return Response({"status": False,  "message": "Your email is not verified. Please verify your email to continue."}, status=status.HTTP_401_UNAUTHORIZED)

                apartment = models.Apartment.objects.get(
                    id=serializer.data['apartment_id'])
                user_email = user['data']['email']
                if apartment.isOccupied:
                    return Response({"status": False, "message": "This apartment is full"})

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
                    payment_reference=reference,
                    payment_link=authorization_url,
                    email=user_email,
                    first_name=user['data']['first_name'],
                    last_name=user['data']['last_name'],
                    phone_number=user['data']['phone_number'],
                    no_of_guests=request.data['no_of_guests'],
                    cover_photo=apartment.images[0]
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
            except Exception:
                return Response({"status": False, "message": "server error"}, status=status.HTTP_400_BAD_REQUEST)


class VerifyApartmentBooking(APIView):
    """View for verifying apartment booking payment"""

    def post(self, request, *args, **kwargs):
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
            return Response({"status": True, "message": "Payment verified successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": False, "message": "Payment not verified"}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(methods=['PATCH'], exclude=True)
class AddImagesToApartmentView(generics.UpdateAPIView):
    """View for editing apartment listing"""
    serializer_class = serializers.ApartmentImageSerializer

    def patch(self, request, *args, **kwargs):
        pass

        # hobbies = request.data['hobbies']
        # token = request.headers.get('Authorization')
        # try:
        #     payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        # except jwt.ExpiredSignatureError:
        #     raise AuthenticationFailed('unauthenticated')
        # user_id = payload['id']
        # user = models.CustomUser.objects.filter(id=user_id).first()
        # if user is None:
        #     return Response({'status': False, 'message':'user not found'})
        # print("hobbies",user.hobbies)
        # user.hobbies.update(hobbies)
        # user.save()
        # serializer = serializers.UserSerializer(user)
        # return Response({"status":True, "message":"user hobbies updated successfully","data":serializer.data})

        """
            upload images to cloudinary
            save the links to the images on the db
            need an API that takes in the images
            sends images to cloudinary
            saves the link
        """


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
    queryset = models.Apartment.objects.filter(isOccupied=False)

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


class ApartmentDetailView(generics.RetrieveAPIView):
    """View for getting the details of one apartment"""
    serializer_class = serializers.ApartmentSerializer

    def get(self, request, *args, **kwargs):
        try:
            apartment_id = self.kwargs.get('id')
            apartment = models.Apartment.objects.filter(
                id=apartment_id).first()
            serializer = self.serializer_class(apartment)
            return Response({"status": True, "message": "Apartment retrieved successfully", "data": serializer.data}, status=status.HTTP_200_OK)
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
            if token is None:
                raise AuthenticationFailed("unauthenticated")
            try:
                user = user_service.get_user(token=token)
                user_id = user['data']['id']
                verified_status = user['data']['isVerified']
            except Exception:
                return Response({"status": False, "message": "unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
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
                if token is None:
                    raise AuthenticationFailed("unauthenticated")
                try:
                    user = user_service.get_user(token=token)
                    user_id = user['data']['id']
                except Exception:
                    return Response({"status": False, "message": "unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
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
            except Exception:
                return Response({"status": False, "message": "Server Error"}, status=status.HTTP_400_BAD_REQUEST)


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


class MaintainanceRequestView(generics.CreateAPIView):
    serializer_class = serializers.MaintainanceRequestSerializer
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            # try:
            token = request.headers.get('Authorization')
            if token is None:
                raise AuthenticationFailed("unauthenticated")
            try:
                user = user_service.get_user(token=token)
                user_id = user['data']['id']
                user_email = user['data']['email']
                verified_status = user['data']['isVerified']
            except Exception:
                return Response({"status": False, "message": "unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
            if not verified_status:
                return Response({"status": False,  "message": "Your email is not verified. Please verify your email to continue."}, status=status.HTTP_401_UNAUTHORIZED)

            apartment = get_user_current_apartment(user_id)
            maintenance_request = models.Maintainance.objects.create(
                apartment_id=apartment,
                user_id=user_id,
                name=serializer.data.get('name'),
                phone_number=serializer.data.get('phone_number'),
                maintenance_category=serializer.data.get(
                    'maintenance_category'),
                maintenance_type=serializer.data.get('maintenance_type'),
                description=serializer.data.get('description')
            )

            send_maintenance_request_email(user_email, apartment.address)
            return Response({"status": True, "message": "Maintainance request sent successfully."}, status=status.HTTP_200_OK)

            # except Exception:
            #     return Response({"status": False, "message": "server error"}, status=status.HTTP_400_BAD_REQUEST)


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


class UserMaintainanceHistoryView(generics.ListAPIView):
    serializer_class = serializers.MaintainanceSerializer
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        try:
            token = request.headers.get('Authorization')
            if token is None:
                raise AuthenticationFailed("unauthenticated")
            try:
                user = user_service.get_user(token=token)
                user_id = user['data']['id']
                verified_status = user['data']['isVerified']
            except Exception:
                return Response({"status": False, "message": "unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
            if not verified_status:
                return Response({"status": False,  "message": "Your email is not verified. Please verify your email to continue."}, status=status.HTTP_401_UNAUTHORIZED)

            queryset = models.Maintainance.objects.filter(user_id=user_id)
            qs = self.serializer_class(queryset, many=True)
            return Response({"status": True, "message": "Data retrieved successfully", "data": qs.data}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"status": False, "message": "server error"}, status=status.HTTP_400_BAD_REQUEST)


class TransactionDetailsView(generics.RetrieveAPIView):
    serializer_class = serializers.TransactionSerializer
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        try:
            token = request.headers.get('Authorization')
            if token is None:
                raise AuthenticationFailed("unauthenticated")
            try:
                user = user_service.get_user(token=token)
                user_id = user['data']['id']
                verified_status = user['data']['isVerified']
            except Exception:
                return Response({"status": False, "message": "unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
            if not verified_status:
                return Response({"status": False,  "message": "Your email is not verified. Please verify your email to continue."}, status=status.HTTP_401_UNAUTHORIZED)

            trnx_id = self.kwargs.get('id')
            queryset = models.Transaction.objects.filter(id=trnx_id).first()
            qs = self.serializer_class(queryset)
            return Response({"status": True, "message": "Data retrieved successfully", "data": qs.data}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"status": False, "message": "server error"}, status=status.HTTP_400_BAD_REQUEST)


class TransactionHistoryView(generics.ListAPIView):
    serializer_class = serializers.TransactionSerializer
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        try:
            token = request.headers.get('Authorization')
            if token is None:
                raise AuthenticationFailed("unauthenticated")
            try:
                user = user_service.get_user(token=token)
                user_id = user['data']['id']
                verified_status = user['data']['isVerified']
            except Exception:
                return Response({"status": False, "message": "unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
            if not verified_status:
                return Response({"status": False,  "message": "Your email is not verified. Please verify your email to continue."}, status=status.HTTP_401_UNAUTHORIZED)

            queryset = models.Transaction.objects.filter(user_id=user_id)
            qs = self.serializer_class(queryset, many=True)
            return Response({"status": True, "message": "Data retrieved successfully", "data": qs.data}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"status": False, "message": "server error"}, status=status.HTTP_400_BAD_REQUEST)
