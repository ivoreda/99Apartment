from django.urls import path
from . import views

urlpatterns = [
    # Not for users
    path('list-apartment/', views.ListApartmentView.as_view(), name='list-apartment'),
    path('unlist-apartment/', views.UnlistApartmentView.as_view(), name='unlist-apartment'),
    path('edit-apartment/', views.EditApartmentView.as_view(), name='edit-apartment'),

    # For users
    path('book-apartment/', views.BookApartmentView.as_view(), name='book-apartment'),
    path('book-apartment-inpection/', views.BookApartmentInspectionView.as_view(), name='book-apartment-inpection'),
    path('<int:id>/', views.ApartmentDetailView.as_view(), name='apartment-detail'),
    path('', views.PaginatedListApartmentView.as_view(), name='all-apartment'),
    path('apartment-inpection/', views.GetApartmentInspectionView.as_view(), name='apartment-inpection'),



]