from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_results, name='search_results'),
    path('station/<int:pk>/', views.station_detail, name='station_detail'),
    path('register/', views.register_owner, name='register_owner'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('dashboard/add/', views.add_station, name='add_station'),
    path('dashboard/edit/<int:pk>/', views.edit_station, name='edit_station'),
    path('dashboard/delete/<int:pk>/', views.delete_station, name='delete_station'),
]
