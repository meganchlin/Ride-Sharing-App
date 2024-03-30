# Django Web-App: Ride Sharing Service

This web application is built using Django and provides functionalities for users to request, drive for, and join rides. It supports three roles:

### Ride Owner
- Requests a ride by specifying destination address, required arrival date & time, total number of passengers, vehicle type, and any special requests.
- Can modify a ride request until it is confirmed.
- Can view ride status until the ride is complete.

### Ride Driver
- Registers as a driver with vehicle information including type, license plate number, maximum passengers, and special vehicle info.
- Can search for open ride requests based on attributes and claim and start a ride service.
- Can complete rides.

### Ride Sharer
- Searches for open ride requests based on destination, arrival window, and number of passengers.
- Can join a ride and view ride status.

## Functionality

- **Create Account**: Users can create an account if they do not have one.
- **Login/Logout**: Users with an account can log in and log out.
- **Driver Registration**: Logged-in users can register as a driver and enter personal and vehicle info.
- **Ride Selection**: Users can select which ride they want to perform actions on.
- **Ride Requesting**: Users can request a ride by specifying various attributes.
- **Ride Request Editing (Owner)**: Ride owners can edit requested attributes as long as the ride is not confirmed.
- **Ride Status Viewing (Owner/Sharer)**: Ride owners or sharers can view the status of their non-complete rides.
- **Ride Status Viewing (Driver)**: Ride drivers can view the status of their confirmed rides and mark them as complete.
- **Ride Searching (Driver)**: Drivers can search for open ride requests based on vehicle capacity and attributes specified in the ride request.
- **Ride Searching (Sharer)**: Sharers can search for open ride requests and join selected rides.
