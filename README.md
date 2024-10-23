# TP Flask, REST et OpenAPI

## Overview
This project implements a simple cinema management system with 4 microservices that all use REST API:

1. **Movie**: Manages movie data.
2. **Times**: Manages movie showtimes.
3. **Booking**: Handles user bookings and checks showtime availability via `Times`.
4. **User**: Entry point for users, allowing them to retrieve movie details and make reservations using `Booking` and `Movie`.

## Setup
Install dependencies:

```bash
pip install -r requirements.txt
```
## Major Changes

- **Movie Service Enhancements**: Added new endpoints to retrieve additional movie information and implemented a `/help` endpoint to list all available endpoints in the Movie service. The OpenAPI specification has been updated accordingly.

- **Times Microservice Development**: Developed the Times microservice based on the provided OpenAPI specification (`UE-archi-distribuees-Showtime-1.0.0-resolved.yaml`). 

- **Booking Microservice Implementation**: Coded the Booking service following the OpenAPI specification (`UE-archi-distribuees-Booking-1.0.0-resolved.yaml`). 

- **User Microservice Design**: Reviewed the `user.json` file and devised an OpenAPI specification for the User service, which integrates functionalities from both Booking and Movie services. This includes:
  - An endpoint to retrieve reservations by user name or ID, which queries the Booking service to confirm reservation availability for the requested date.
  - An endpoint to fetch movie details associated with a user's reservations, requiring queries to both Booking and Movie services.

- **User Microservice Implementation**: The User microservice has been implemented to manage user-related functionalities in the cinema application. It provides an interface to retrieve user information, manage bookings, and fetch movie details associated with those bookings. The service reads user data from a JSON file and communicates with the Booking and Movie microservices to facilitate actions such as retrieving booking information and making new reservations.

Testing was performed using Postman to ensure that all functionalities are operational and respond as expected.
