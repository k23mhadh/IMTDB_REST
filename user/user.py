from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

with open('{}/databases/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the User service!</h1>"

# Route to get all users in JSON format
@app.route("/users", methods=['GET'])
def get_users():
    res = make_response(jsonify(users), 200)
    return res

# Route to get a specific user by their ID
@app.route("/users/<userid>", methods=['GET'])
def get_user_byid(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            res = make_response(jsonify(user),200)
            return res
    return make_response(jsonify({"error":"User not found"}),400)

# Route to fetch all movies from the movie service
@app.route("/movies", methods=['GET'])
def get_movies():
    
    movies_url = "http://localhost:3200"
    movies_response = requests.get(movies_url + "/json")
    print(movies_response)
    return make_response(movies_response.json(),200)

# Route to get all bookings for a specific user by their ID
@app.route("/myBookings/<userId>", methods=['GET'])
def get_myBookings(userId):
    bookings_url = "http://localhost:3201"
    bookings_response = requests.get(bookings_url + "/bookings/"+userId)
    return make_response(bookings_response.json(),200)

# Route to create a booking for a specific user by their ID, booking date, and movie ID
@app.route("/makeBooking/<userId>/<date>/<movie_id>", methods=['GET'])
def make_booking(userId, date, movie_id):
    bookings_url = "http://localhost:3201"
    json_data = { "date" : date, "movieid" : movie_id } 
    bookings_response = requests.post(bookings_url + "/bookings/" + userId, json = json_data)
    return make_response(jsonify({"success":"True","data":bookings_response.json()}),200)

# Route to get detailed booking and movie information for a specific user
@app.route("/bookingInfo/<userId>", methods=['GET'])
def get_booking_info(userId):
    bookings_url = "http://localhost:3201"
    movies_url = "http://localhost:3200"
    
    # Get bookings for the user
    bookings_response = requests.get(bookings_url + "/bookings/" + userId)
    
    # Check if bookings request was successful
    if bookings_response.status_code != 200:
        return make_response(jsonify({"error": "Failed to fetch bookings"}), bookings_response.status_code)
    
    bookings_data = bookings_response.json()
    dates = bookings_data.get("dates", [])
    
    movies = []
    for date in dates:
        movies += date.get("movies", [])
    
    movies_info = []
    
    # Fetch movie information for each booked movie
    for movie_id in movies:
        movie_response = requests.get(movies_url +"/movies/" + movie_id)
        
        # Check if movie request was successful
        if movie_response.status_code == 200:
            movies_info.append(movie_response.json())  # Add the movie details
        else:
            # Handle failed movie fetch 
            movies_info.append({"movie_id": movie_id, "error": "Failed to fetch movie info"})
    
    # Return all movie information as a JSON response
    return make_response(jsonify(movies_info), 200)
       
if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
