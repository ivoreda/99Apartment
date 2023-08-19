from django.urls import path
from . import views

urlpatterns = [
    # For Hosts
    path('list-apartment/', views.ListApartmentView.as_view(), name='list-apartment'),
    path('delete-apartment/<int:id>/',
         views.DeleteApartmentView.as_view(), name='delete-apartment'),
    path('unlist-apartment/', views.UnlistApartmentView.as_view(),
         name='unlist-apartment'),
    path('save-draft/', views.SaveApartmentDraftView.as_view(), name='save-draft'),
    path('amenities/', views.GetApartmentAmenitiesView.as_view(), name='amenities'),
    path('rules/', views.GetApartmentRulesView.as_view(), name='rules'),
    path('edit-apartment/', views.EditApartmentView.as_view(), name='edit-apartment'),
    path('all-host-apartment/', views.HostApartmentListView.as_view(),
         name='all-host-apartments'),
    path('all-host-apartment-maintenance/', views.HostApartmentMaintenanceListView.as_view(),
         name='all-host-apartment-maintenance'),


    # For Guests
    path('book/', views.BookApartmentView.as_view(), name='book'),
    path('verify-booking/<str:reference>', views.VerifyApartmentBooking.as_view(),
         name='verify-booking'),
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

    path('maintainance-request/', views.MaintenanceRequestView.as_view(),
         name='maintainance-request'),
    path('user/maintainance-history/', views.UserMaintenanceHistoryView.as_view(),
         name='user-maintainance-history'),

    path('transaction-details/<int:id>',
         views.TransactionDetailsView.as_view(), name='transaction-details'),
    path('user/transactions/', views.TransactionHistoryView.as_view(),
         name='user-transaction-history'),


]
