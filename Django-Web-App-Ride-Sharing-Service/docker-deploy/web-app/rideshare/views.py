from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from .models import User, Driver, Ride, RideStatus, Sharer
from .forms import SignupForm, DriverForm, SharerForm, OwnerEditForm, OwnerRequestForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, F, Value, IntegerField
from django.db.models.functions import Coalesce

import os.path
import base64

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import datetime
from django.utils import timezone



# Renders the HTML template with the data in the context variable
def signup(request):
    form = SignupForm()

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = SignupForm(request.POST)
        print(form.errors)

        # Check if the form is valid:
        if form.is_valid():
            print("valid")
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            user = form.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('rideshare:login') )

    # If this is a GET (or any other method) create the default form.       
    return render(request, 'signup.html', {'form': form})

def userLogin(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            # Redirect to a success page.
            return HttpResponseRedirect(reverse('rideshare:index') )
        else:
            messages.error(request,'username or password not correct')
            return HttpResponseRedirect(reverse(('rideshare:login')))
    return render(request, "login.html")

@login_required()
def index(request):
    """View function for home page of site."""
    user = request.user

    num_rides = Ride.objects.filter(owner_id=user.id).count()
    num_drivers = Driver.objects.filter(user=user).count()
    num_sharers = Sharer.objects.filter(user=user).count()


    context = {
        'num_rides': num_rides,
        'num_drivers': num_drivers,
        'num_sharers': num_sharers
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


def send_email(subject, to_email, html_content):
    try:
        sg = SendGridAPIClient('')
        message = Mail(
            from_email='alejandroyiweihe@gmail.com',
            to_emails=to_email,
            subject=subject,
            html_content=html_content
        )
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(f"Error sending email: {str(e)}")


# Driver
class DriverView(LoginRequiredMixin):

    @login_required()
    def updateRideStatus(request, ride_id, status):
        ride = get_object_or_404(Ride, pk = ride_id)
        driver = get_object_or_404(Driver, user=request.user)

        ride.status = status
        ride.driver = driver

        ride.save()

        if status == RideStatus.CONFIRMED.value:
            subject = "Ride Confirmed"
            to_email = ride.owner.email
            html_content = f"""
                    <h1>Dear {ride.owner.first_name} {ride.owner.last_name},</h1>
                    <h1>Your ride to {ride.destination_address} has been confirmed.</h1>
                    <h1>Your driver is {driver.name}.</h1>
                """
            send_email(subject, to_email, html_content)
        return HttpResponseRedirect(reverse('rideshare:driverMain'))

    @login_required()
    def driverRegister(request):
        user = request.user

        # Try to get the existing Driver instance, or create a new one if it doesn't exist
        try:
            driver = Driver.objects.get(user=user)
            form = DriverForm(instance=driver)
        except Driver.DoesNotExist:
            driver = None
            form = DriverForm()
        
        # If this is a POST request then process the Form data
        if request.method == 'POST':

            # Create a form instance and populate it with data from the request (binding):
            form = DriverForm(request.POST, instance=driver)

            # Check if the form is valid:
            if form.is_valid():
                form.instance.user = user
                driver = form.save()

                # redirect to a new URL:
                return HttpResponseRedirect(reverse('rideshare:driverMain') )

        # If this is a GET (or any other method) create the default form.       
        return render(request, "rideshare/driver/register.html", {'form': form})

    @login_required()
    def driverEdit(request):
        driver = get_object_or_404(Driver, user = request.user)
        form = DriverForm(instance=driver)

        # If this is a POST request then process the Form data
        if request.method == 'POST':

            # Create a form instance and populate it with data from the request (binding):
            form = DriverForm(request.POST, instance=driver)

            # Check if the form is valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
                driver = form.save()

                # redirect to a new URL:
                return HttpResponseRedirect(reverse('rideshare:driverMain') )

        # If this is a GET (or any other method) create the default form.       
        return render(request, "rideshare/driver/edit.html", {'form': form})

    @login_required()
    def driverMain(request):
        if Driver.objects.filter(user=request.user).count() == 0:
            return HttpResponseRedirect(reverse('rideshare:driverRegister') )
        driver = get_object_or_404(Driver, user=request.user)
        #driver = Driver.objects.get(user=request.user)
        rides = Ride.objects.filter(driver=driver, status=RideStatus.CONFIRMED.value).order_by('required_arrival_time')
        complete_rides = Ride.objects.filter(driver=driver, status=RideStatus.COMPLETE.value).order_by('id')
        return render(request, "rideshare/driver/main.html", {'rides': rides, 'complete_rides': complete_rides})

    @login_required()
    def driverSearch(request):
        driver = get_object_or_404(Driver, user=request.user)
        if request.method == 'GET':
            if request.GET.get('arrival_time') == "":
                arrival_time = datetime.datetime.now()
            else:
                arrival_time_str = request.GET.get('arrival_time')
                arrival_time = datetime.datetime.strptime(arrival_time_str, "%Y-%m-%d %H:%M")
                
            if request.GET.get('passenger_count') == "":
                passenger_count = driver.capacity
            else:
                passenger_count = int(request.GET.get('passenger_count'))
            destination = request.GET.get('destination', "")

            if passenger_count > driver.capacity:
                passenger_count = driver.capacity
            

            #if passenger_count > driver.capacity:
            #    raise ValidationError("Passenger count exceed your vehicle's capacity.")

            # Perform your search logic based on form input
            results = Ride.objects.filter(
                required_arrival_time__gte=arrival_time,
                vehicle_type=driver.vehicle_type,
                status=RideStatus.OPEN.value,
                special_requests=driver.special_vehicle_info,
                destination_address__contains=destination,
            )
            # .annotate(
            #     total_passengers=Coalesce(Sum('sharer__num_passengers'), Value(0), output_field=IntegerField())
            # ).filter(
            #     total_passengers__lte=F('driver__capacity') - F('num_passengers')
            # )
            print(results)

            return render(request, 'rideshare/driver/search.html', {'results': results})
        return render(request, "rideshare/driver/search.html")

# Owner
from django.views import generic
#class OwnerRideListView(generic.ListView):


class OwnerView(LoginRequiredMixin):
 
    def owner_rides_view(request):
        user = request.user
        owner_rides = user.rides_as_owner.all()
        return render(request, "rideshare/ride_list.html", {'ride_list': owner_rides})


    def owner_request_view(request):
        from .models import Ride  # Import the Ride model if not already imported

    def owner_request_view(request):
        user = request.user
        if request.method == 'POST':
            form = OwnerRequestForm(request.POST)
            if form.is_valid():
                new_ride = Ride(
                    destination_address=form.cleaned_data['destination'],
                    required_arrival_time=form.cleaned_data['required_arrival_time'],
                    vehicle_type=form.cleaned_data['vehicle_type'],
                    num_passengers=form.cleaned_data['num_passengers'],
                    shared=form.cleaned_data['shared'],
                    special_requests=form.cleaned_data['special_requests'],  
                    status=RideStatus.OPEN.value,
                    owner=user, 
                )
                new_ride.save()
                return HttpResponseRedirect(reverse('rideshare:owner-rides'))
        else:
            form = OwnerRequestForm()
        return render(request, "rideshare/owner/request_ride.html", {'form': form})


    from django.shortcuts import get_object_or_404

    def owner_edit_view(request, ride_id):
        user = request.user

        # Get the existing ride instance
        existing_ride = get_object_or_404(Ride, pk=ride_id)
        
        if existing_ride.owner != request.user:
            return HttpResponse("You are not the owner of this ride.")


        if request.method == 'POST':
           
            form = OwnerRequestForm(request.POST, instance=existing_ride)

            if form.is_valid():
                
                updated_ride = form.save(commit=False)  
                updated_ride.owner = user
                updated_ride.save()

                # Redirect to a new URL or render a success page
                return HttpResponseRedirect(reverse('rideshare:rides'))

        else:
            # Create the form prepopulated with existing ride details
            form = OwnerRequestForm(instance=existing_ride)

        return render(request, "rideshare/owner/edit_ride.html", {'form': form, 'ride': existing_ride})

    def owner_delete(request, ride_id):
        ride_instance = Ride.objects.get(pk=ride_id)
        ride_instance.delete_ride()
        user = request.user
        owner_rides = user.rides_as_owner.all()
        return render(request, "rideshare/ride_list.html", {'ride_list': owner_rides})


    def ride_detail_view(request, pk):
        try:
            ride = Ride.objects.get(pk=pk)
        except Ride.DoesNotExist:
            raise Http404('Ride does not exist')

        is_owner = ride.owner == request.user
        return render(request, 'rideshare/ride_detail.html', context={'ride': ride, 'is_owner': is_owner})

# Sharer
class SharerView(LoginRequiredMixin):

    @login_required()
    def sharerMain(request):
        share = Sharer.objects.filter(user=request.user)
        rides = share.values_list("ride", flat=True)

        open_rides = []
        confirmed_rides = []
        complete_rides = []
        for ride in rides:
            if Ride.objects.get(id=ride).status == RideStatus.OPEN.value:
                open_rides.append(Ride.objects.get(id=ride))
            elif Ride.objects.get(id=ride).status == RideStatus.CONFIRMED.value:
                confirmed_rides.append(Ride.objects.get(id=ride))
            elif Ride.objects.get(id=ride).status == RideStatus.COMPLETE.value:
                complete_rides.append(Ride.objects.get(id=ride))
        return render(request, "rideshare/sharer/main.html", {'open_rides': open_rides, 'confirmed_rides': confirmed_rides, 'complete_rides': complete_rides})

    

    @login_required()
    def sharerSearch(request):
        if request.method == 'GET':
            if request.GET.get('earliest_arrival_time') == "":
                earliest_arrival_time = datetime.datetime.now()
            else:
                earliest_arrival_time_str = request.GET.get('earliest_arrival_time')
                earliest_arrival_time = datetime.datetime.strptime(earliest_arrival_time_str, "%Y-%m-%d %H:%M")
                earliest_arrival_time = timezone.now() 

            if request.GET.get('latest_arrival_time') == "":
                latest_arrival_time = earliest_arrival_time + datetime.timedelta(hours=1)
            else:
                latest_arrival_time = request.GET.get('latest_arrival_time')

            if request.GET.get('passenger_count') == "":
                passenger_count = 1
            else:
                passenger_count = int(request.GET.get('passenger_count'))
            
            print(request.GET.get('passenger_count'))

            destination = request.GET.get('destination', "")


            results = Ride.objects.filter(
                required_arrival_time__gte=earliest_arrival_time,
                required_arrival_time__lte=latest_arrival_time,
                status=RideStatus.OPEN.value,
                destination_address__contains=destination,
                shared=True
            )

            print(results)

            return render(request, 'rideshare/sharer/search.html', {'rides': results})
        return render(request, "rideshare/sharer/search.html")

    @login_required()
    def shareJoin(request, ride_id):
        user = request.user
        ride = Ride.objects.get(pk=ride_id)
        form = SharerForm()
        
        # If this is a POST request then process the Form data
        if request.method == 'POST':

            # Create a form instance and populate it with data from the request (binding):
            form = SharerForm(request.POST)

            if form.is_valid():
                print("valid")
                tmp = form.save(commit=False)
                tmp.user = user
                tmp.ride = ride
                tmp.save()

            # Check if the form is valid:
            if form.is_valid():
                form.instance.user = user
                driver = form.save()

                # redirect to a new URL:
                return HttpResponseRedirect(reverse('rideshare:sharerMain') )

        # If this is a GET (or any other method) create the default form.       
        return render(request, "rideshare/sharer/join.html", {'form': form})


    @login_required()
    def shareEdit(request, ride_id):
        user = request.user
        ride = Ride.objects.get(id=ride_id)
        shareRide = Sharer.objects.get(ride=ride, user=user)
        form = SharerForm(instance=shareRide)

        
        # If this is a POST request then process the Form data
        if request.method == 'POST':

            submit_action = request.POST.get('submit_action')

            if submit_action == 'Update':
                # Handle Update button click
    
                # Create a form instance and populate it with data from the request (binding):
                form = SharerForm(request.POST, instance=shareRide)

                # Check if the form is valid:
                if form.is_valid():
                    # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
                    sharer = form.save()
            elif submit_action == 'Delete':
                # Handle Delete button click
                shareRide.delete()
                    
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('rideshare:sharerMain') )

        # If this is a GET (or any other method) create the default form.       
        return render(request, "rideshare/sharer/edit.html", {'form': form})


class RideListView(generic.ListView):
    model = Ride


