from django.urls import path
from . import views

urlpatterns = [
    # Not for users
    # path('list-apartment/', views.ListApartmentView.as_view(), name='list-apartment'),
    # path('unlist-apartment/', views.UnlistApartmentView.as_view(), name='unlist-apartment'),
    # path('edit-apartment/', views.EditApartmentView.as_view(), name='edit-apartment'),

    # For users
    path('book/', views.BookApartmentView.as_view(), name='book'),
    path('verify-booking/', views.VerifyApartmentBooking.as_view(),
         name='verify-booking'),
    path('checkout/<str:reference>/', views.CheckoutApartmentView.as_view(), name='checkout'),

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
    path('reviews/<int:id>/',
         views.ApartmentReviewsListView.as_view(), name='apartment-reviews'),

    path('maintainance-request/', views.MaintainanceRequestView.as_view(),
         name='maintainance-request'),
    path('user/maintainance-history/', views.UserMaintainanceHistoryView.as_view(),
         name='user-maintainance-history'),

    path('transaction-details/<int:id>',
         views.TransactionDetailsView.as_view(), name='transaction-details'),
    path('user/transactions/', views.TransactionHistoryView.as_view(),
         name='user-transaction-history'),


]
