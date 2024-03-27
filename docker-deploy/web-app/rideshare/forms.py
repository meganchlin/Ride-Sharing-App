from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Driver, Sharer, VehicleType, Ride

class DriverForm(forms.ModelForm):
    name = forms.CharField(required=True, label="Full Name", max_length=255, widget=forms.TextInput(attrs={'placeholder':"Enter your name"}))
    #vehicle_type = forms.CharField(required=True, label="Vehicle Type", max_length=20, widget=forms.TextInput(attrs={'placeholder':"Enter your vehicle type"}))
    vehicle_type = forms.ChoiceField(choices=[(item.value, item.name) for item in VehicleType])
    capacity = forms.IntegerField(required=True, label="Capacity") #widget=forms.TextInput(attrs={'placeholder':"Enter maximum number of passenger"})
    license_plate_number = forms.CharField(required=True, label="License Plate Number", max_length=20, widget=forms.TextInput(attrs={'placeholder':"Enter license plate number"}))
    special_vehicle_info = forms.CharField(required=False, label="Special Vehicle Info", widget=forms.Textarea(attrs={'placeholder':"Enter special vehicle info"}))

    class Meta:
        model = Driver
        exclude = ["user"]
        widgets = {'user': forms.HiddenInput()}
        labels = {
            "user": ""
        }

class SignupForm(UserCreationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':"Username"}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder':"Password"}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder':"Password Confirmation"}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder':"Email Address"}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':"First Name"}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':"Last Name"}))
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name']

class SharerForm(forms.ModelForm):
    destination = forms.CharField(max_length=255)
    num_passengers = forms.IntegerField()
    earliest_arrival_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    latest_arrival_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    

    class Meta:
        model = Sharer
        fields = ['destination', 'num_passengers', 'earliest_arrival_time', 'latest_arrival_time']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set a minimum value for num_passengers (adjust the value accordingly)
        self.fields['num_passengers'].widget.attrs['min'] = 1

class OwnerRequestForm(forms.ModelForm):
    destination = forms.CharField(required=True, label="Destination", max_length=255)
    
    num_passengers = forms.IntegerField(required=True, label="Number of Passengers")
    
    required_arrival_time = forms.DateTimeField(
        required=True,
        label="Required Arrival Time",
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
    )
   
    vehicle_type = forms.ChoiceField(
        choices=[(item.value, item.name) for item in VehicleType],
        required=True,
        label="Vehicle Type"
    )
    shared = forms.BooleanField(
        required=False,  
        initial=False, 
        label="Shared"
    )
    special_requests = forms.CharField(
        required=False,
        label="Special Requests",
        widget=forms.Textarea(attrs={'placeholder': "Enter special requests"}),
    )

    class Meta:
        model = Ride
        fields = [
            'destination',
            'num_passengers',
            'required_arrival_time',
            'vehicle_type',
            'shared',
            'special_requests',
        ]

class OwnerEditForm(forms.ModelForm):
    destination = forms.CharField(required=True, label="Destination", max_length=255)
    
    num_passengers = forms.IntegerField(required=True, label="Number of Passengers")
    
    required_arrival_time = forms.DateTimeField(
        required=True,
        label="Required Arrival Time",
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
    )
   
    vehicle_type = forms.ChoiceField(
        choices=[(item.value, item.name) for item in VehicleType],
        required=True,
        label="Vehicle Type"
    )
    shared = forms.BooleanField(
        required=False,  
        initial=False, 
        label="Shared"
    )
    special_requests = forms.CharField(
        required=False,
        label="Special Requests",
        widget=forms.Textarea(attrs={'placeholder': "Enter special requests"}),
    )

    class Meta:
        model = Ride
        fields = [
            'destination_address',
            'num_passengers',
            'required_arrival_time',
            'vehicle_type',
            'shared',
            'special_requests',
        ]

