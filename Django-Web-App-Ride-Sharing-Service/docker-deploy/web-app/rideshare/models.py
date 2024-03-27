from django.db import models
from django.contrib.auth.models import User
from enum import Enum
import uuid 


class VehicleType(Enum):
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'

class RideStatus(Enum):
    OPEN = 'Open'
    CONFIRMED = 'Confirmed'
    COMPLETE = 'Complete'

class Sharer(models.Model):

    destination = models.CharField(max_length=255)
    earliest_arrival_time = models.DateTimeField()
    latest_arrival_time = models.DateTimeField()
    num_passengers = models.IntegerField()

    # ForeignKey field for Ride
    ride = models.ForeignKey('Ride', on_delete=models.CASCADE)

    # ForeignKey field for User
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Sharer to {self.destination}'

class Driver(models.Model):

    name = models.CharField(max_length=255)
    vehicle_type = models.CharField(
        max_length=20,
        choices=[(item.value, item.name) for item in VehicleType],
        default=VehicleType.SMALL.value
    )
    capacity = models.IntegerField()
    license_plate_number = models.CharField(max_length=20)
    special_vehicle_info = models.TextField(blank=True, null=True)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE) 

    def __str__(self):
        return self.name

from datetime import datetime

class Ride(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
    destination_address = models.CharField(max_length=255)
    required_arrival_time = models.DateTimeField(default=datetime(2024, 12, 31, 23, 59, 59))
    vehicle_type = models.CharField(
        max_length=20,
        choices=[(item.value, item.name) for item in VehicleType],
        default=None  # Default to 'small' if not specified
    )

    num_passengers = models.IntegerField()
    shared = models.BooleanField()
    special_requests = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=[(item.value, item.name) for item in RideStatus],
        default=RideStatus.OPEN.value
    )
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rides_as_owner')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='rides_as_driver', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('ride-detail', args=[str(self.id)])

    def delete_ride(self):
        """Delete this ride instance."""
        self.delete()
        
    def __str__(self):
        return f'Ride to {self.destination_address}'
