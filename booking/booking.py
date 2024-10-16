from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'


with open('{}/databases/bookings.json'.format("."), "r") as jsf:
   bookings = json.load(jsf)["bookings"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"

@app.route("/bookings", methods=['GET'])
def get_json():
   return  make_response(jsonify(bookings), 200)
   
   
@app.route("/bookings/<userid>", methods=['GET'])
def get_booking_for_user(userid):
   for booking in bookings:
      if str(booking["userid"]) == str(userid):
         res = make_response(jsonify(booking),200)
         return res
   return make_response(jsonify({"error":"Bad input parameter"}),400)

@app.route("/bookings/<userid>", methods=['POST'])
def add_booking_byuser(userid):
   req = request.get_json()
   date = req['date']
   movieid = req['movieid']
   
   # Validate req..
   
   showtimes_url = "http://192.168.43.226:3202"
   showtimes_response = requests.get(showtimes_url + "/showmovies/" + date)
   if showtimes_response.status_code != 200:
      return make_response(jsonify({"error": "Failed to retrieve showtimes"}), 400)
   showtimes_data = showtimes_response.json()
   if movieid not in showtimes_data['movies']:
      return make_response(jsonify({"error": "Movie not found for the given date"}), 400)

    # Check if the booking already exists
   for booking in bookings:
      if str(booking["userid"]) == str(userid):
         for date_obj in booking["dates"]:
               if date_obj["date"] == date and movieid in date_obj["movies"]:
                  return make_response(jsonify({"error": "An existing item already exists"}), 409)


   # If the booking doesn't exist, create a new one
   existing_booking = next((booking for booking in bookings if str(booking["userid"]) == str(userid)), None)
   if existing_booking:
      existing_date_obj = next((date_obj for date_obj in existing_booking["dates"] if date_obj["date"] == date), None)
      if existing_date_obj:
         existing_date_obj["movies"].append(movieid)

      else:
         existing_booking["dates"].append({"date": date, "movies": [movieid]})

   else:
      bookings.append({
         "userid": userid,
         "dates": [
               {
                  "date": date,
                  "movies": [movieid]
               }
         ]
      })
      write(bookings)
   return make_response(jsonify({"message": "Booking created"}), 200)


def write(bookings):
    with open('{}/databases/bookings.json'.format("."), 'w') as f:
      resFile = {"bookings":bookings}
      json.dump(resFile, f)

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
