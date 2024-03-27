from django.urls import path, include
from . import views

app_name = "rideshare"
urlpatterns = [
    # Can use reverse URL mapping such as: <a href="{% url 'index' %}">Home</a> to make a hyperlink to the page
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('login', views.userLogin, name='login'),

    path("driver/register", views.DriverView.driverRegister, name="driverRegister"),
    path("driver/edit", views.DriverView.driverEdit, name="driverEdit"),
    path("driver/main", views.DriverView.driverMain, name="driverMain"),
    path("driver/search", views.DriverView.driverSearch, name="driverSearch"),
    path("<uuid:ride_id>/update/<str:status>", views.DriverView.updateRideStatus, name="updateRideStatus"),

    path("sharer/main", views.SharerView.sharerMain, name = "sharerMain"),
    path("sharer/search", views.SharerView.sharerSearch, name="sharerSearch"),
    path("sharer/<uuid:ride_id>/join", views.SharerView.shareJoin, name="sharerJoin"),
    path("sharer/<uuid:ride_id>/edit", views.SharerView.shareEdit, name="sharerEdit"),
    
    path('rides', views.RideListView.as_view(), name='rides'),
    path('rides/<uuid:pk>/', views.OwnerView.ride_detail_view, name='ride-detail'),

    path("owner/rides", views.OwnerView.owner_rides_view, name="owner-rides"),
    path("owner/request", views.OwnerView.owner_request_view, name="owner-request"),
    path("owner/edit/<uuid:ride_id>/", views.OwnerView.owner_edit_view, name="owner-edit"),
    path("owner/delete/<uuid:ride_id>/", views.OwnerView.owner_delete, name="owner-delete")
]
