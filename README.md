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
