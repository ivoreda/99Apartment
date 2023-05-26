from rest_framework import generics
from rest_framework.views import APIView

from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed

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
            token = request.headers.get('Authorization')
            if token is None:
                return Response({"error": True, "message": "unauthenticated"})
            user = user_service.get_user(token=token)
            apartment = models.Apartment.objects.get(
                id=serializer.data['apartment_id'])
            user_id = user['data']['id']
            user_email = user['data']['email']
            if apartment.isOccupied:
                return Response({"status": False, "message": "This apartment is full"})

            paystack_response = paystack_api.initialise_transaction(
                email=user_email, amount=apartment.total_price)
            authorization_url = paystack_response['data']['authorization_url']
            reference = paystack_response['data']['reference']

            booking = models.ApartmentBooking.objects.create(
                apartment_id=apartment,
                user_id=user_id,
                start_date=request.data['start_date'],
                end_date=request.data['end_date'],
                payment_reference=reference
            )

            # send email to user after apartment has been booked

            # save transaction details after apartment has been booked
            trnx_details = models.Transaction.objects.create(
                user_id=user_id,
                amount=apartment.total_price,
                payment_reference=reference,
                transaction_status="pending",
                description="Apartment Boooking",
                recipient="99Apartment",
                payment_method="PayStack",
            )

            return Response({"message": "Apartment booked successfully", "data": {"authorization_url": authorization_url, "reference": reference}}, status=status.HTTP_201_CREATED)
        # except Exception:
        #     return Response({"error": True, "message": "server error"}, status=status.HTTP_400_BAD_REQUEST)


class VerifyApartmentBooking(APIView):
    """View for verifying apartment booking payment"""
    serializer_class = serializers.VerifyApartmentBookingSerializer
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            token = request.headers.get('Authorization')
            if token is None:
                return Response({"error": True, "message": "unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
            try:
                user = user_service.get_user(token=token)
                user_id = user['data']['id']
            except Exception:
                return Response({"error": True, "message": "unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            payment_reference = serializer.data.get('payment_reference')

            paystack_payment_verification_status = paystack_api.verify_transaction(
                reference=payment_reference)
            if paystack_payment_verification_status['data']['status'] == True:
                apartment_booking = models.ApartmentBooking.objects.filter(
                    payment_reference=payment_reference).first()
                apartment_id = apartment_booking.apartment_id
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
                return Response({"status": True, "message": "Payment verified successfully"})
            else:
                return Response({"status": False, "message": "Payment not verified"})


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
        city = self.kwargs.get('city')
        no_of_rooms = self.kwargs.get('no_of_rooms')
        items = models.Apartment.objects.filter(
            city=city, number_of_rooms=no_of_rooms)
        serializer = serializers.ResponseSerializer({"data": items})
        return Response(serializer.data)



class PaginatedListApartmentView(generics.ListAPIView):
    """View for listing all apartments"""
    serializer_class = serializers.ApartmentSerializer
    queryset = models.Apartment.objects.filter(isOccupied=False)

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = serializers.ResponseSerializer({"data": queryset})
            return Response(serializer.data)
        except Exception:
            return Response({"status": False, "message": "server error"}, status=status.HTTP_400_BAD_REQUEST)


class ApartmentDetailView(generics.RetrieveAPIView):
    """View for getting the details of one apartment"""
    serializer_class = serializers.ApartmentSerializer

    def get(self, request, *args, **kwargs):
        try:
            apartment_id = self.kwargs.get('id')
            apartment = models.Apartment.objects.filter(
                id=apartment_id).first()
            serializer = self.serializer_class(apartment)
            return Response({"status": True, "message": "Apartment retrieved successfully", "data": serializer.data})
        except Exception:
            return Response({"status": False, "message": "server error"}, status=status.HTTP_400_BAD_REQUEST)


class BookApartmentInspectionView(generics.CreateAPIView):
    """View for booking apartment inspection"""
    serializer_class = serializers.BookApartmentInsectionSerializer
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            token = request.headers.get('Authorization')
            if token is None:
                raise AuthenticationFailed("unauthenticated")
            user = user_service.get_user(token=token)
            user_id = user['data']['id']
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
            try:
                send_apartment_inspection_email(
                    user_email, address, inspection_date=request.data['inspection_date'])
            except Exception:
                return Response({"status": False, "message": "Server Error"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"status": True, "message": "Inspection booked successfully"})


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
        'inspection/emails/apartment-email-booking-complete.html', {'email': user_email, 'address': address, 'inspection_date': inspection_date})
    email_verification_email = EmailMessage(
        subject, email_template, from_email, [user_email]
    )
    email_verification_email.fail_silently = True
    email_verification_email.send()


class ApartmentReviewsListView(generics.ListAPIView):
    """View for getting an apartments reviews"""
    serializer_class = serializers.GetApartmentReviewsSerializer
    # queryset = models.ApartmentReview.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            apartment_id = self.kwargs.get('id')
            reviews = models.ApartmentReview.objects.filter(
                apartment_id_id=apartment_id)
            reviewed_apartment = models.Apartment.objects.filter(
                id=apartment_id).first()
            number_of_reviews = reviewed_apartment.number_of_reviews

            serializer = self.serializer_class(reviews, many=True)
            return Response({"status": True, "message": "Data retrieved successfully", "number_of_reviews": number_of_reviews, "data": serializer.data})
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
                user = user_service.get_user(token=token)
                user_id = user['data']['id']
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
                return Response({"status": True, "message": "Apartment reviewed successfully"})
            except Exception:
                return Response({"status": False, "message": "Server Error"}, status=status.HTTP_400_BAD_REQUEST)


class GetApartmentCitiesView(generics.ListAPIView):
    """View for getting an apartments locations"""
    serializer_class = serializers.ApartmentCitiesSerializer

    def get(self, request, *args, **kwargs):
        apartment_cities = models.Apartment.objects.all().values()
        cities = []
        for i in apartment_cities:
            cities.append(i['city'])
        return Response({"status": True, "message": "Data retrieved successfully", "data": {"number_of_cities": len(cities), "cities": cities}})
