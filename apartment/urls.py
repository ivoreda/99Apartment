from django.urls import path
from . import views


host_urls = [
    path('list-apartment/', views.ListApartmentView.as_view(), name='list-apartment'),

    path('delete-apartment/<int:id>/',
         views.DeleteApartmentView.as_view(), name='delete-apartment'),

    path('unlist-apartment/', views.UnlistApartmentView.as_view(),
         name='unlist-apartment'),

    path('save-draft/', views.SaveApartmentDraftView.as_view(), name='save-draft'),

    path('publish-draft/<int:id>/', views.PublishDraftApartmentView.as_view(),
         name='publish-draft'),

    path('amenities/', views.GetApartmentAmenitiesView.as_view(), name='amenities'),

    path('rules/', views.GetApartmentRulesView.as_view(), name='rules'),

    path('safety-and-security/', views.GetApartmentSafetyAndSecurityItemsView.as_view(),
         name='safety-and-security'),

    path('additional-charges/', views.GetApartmentAdditionalChargesView.as_view(),
         name='additional-charges'),

    path('cancellation-policy/', views.GetApartmentCancellationPolicyView.as_view(),
         name='cancellation-policy'),

    path('edit-apartment/<int:id>/',
         views.EditApartmentView.as_view(), name='edit-apartment'),

    path('all-host-apartment/', views.HostApartmentListView.as_view(),
         name='all-host-apartments'),

    path('host-apartment/<int:id>/',
         views.HostApartmentByIdView.as_view(), name='host-apartment'),

    path('all-host-apartment-maintenance/', views.HostApartmentMaintenanceListView.as_view(),
         name='all-host-apartment-maintenance'),

    path('services/', views.GetAllServicesView.as_view(), name='services'),

    path('host-analytics', views.HostAnalyticsView.as_view(),
         name='host-analytics'),

    path('host-analytics-dummy', views.HostAnalyticsDummyView.as_view(),
         name='host-analytics'),



]

guest_urls = [
    path('book/', views.BookApartmentView.as_view(), name='book'),
    path('verify-booking/<str:reference>', views.VerifyApartmentBooking.as_view(),
         name='verify-booking'),

    # Paystack webhook
    path('webhook/paystack/', views.PaystackWebhookView.as_view(),
         name='paystack_webhook'),

    path('checkout/<str:reference>/',
         views.CheckoutApartmentView.as_view(), name='checkout'),
    path('book-apartment-inpection/', views.BookApartmentInspectionView.as_view(),
         name='book-apartment-inpection'),
    path('<int:id>/', views.ApartmentDetailView.as_view(), name='apartment-detail'),
    path('', views.PaginatedListApartmentView.as_view(), name='all-apartment'),
    #     path('search-for-apartments/', views.SearchApartmentView.as_view(), name='search-for-apartment'),
    path('apartment-inpection/', views.GetApartmentInspectionView.as_view(),
         name='apartment-inpection'),

    path('cities/', views.GetApartmentCitiesView.as_view(),
         name='cities'),

    path('review/', views.ReviewApartmentView.as_view(),
         name='review'),

    path('reviews/<int:apartment_id>/',
         views.ApartmentReviewsListView.as_view(), name='apartment-reviews'),

    path('maintenance-request/', views.MaintenanceRequestView.as_view(),
         name='maintenance-request'),

    path('user/maintenance-history/', views.UserMaintenanceHistoryView.as_view(),
         name='user-maintenance-history'),

    path('transaction-details/<int:id>',
         views.TransactionDetailsView.as_view(), name='transaction-details'),

    path('user/transactions/', views.TransactionHistoryView.as_view(),
         name='user-transaction-history'),

    path('user/dashboard/', views.UserDashboardView.as_view(), name='user-dashboard'),

    path('change-apartment/', views.ChangeApartmentView.as_view(),
         name='change-apartment'),

    path('get-user-current-apartment/', views.GetUserCurrentApartmentView.as_view(),
         name='get-user-current-apartment'),

]


urlpatterns = host_urls + guest_urls
