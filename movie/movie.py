from flask import Flask, render_template, request, jsonify, make_response
import json
import sys
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3200
HOST = '0.0.0.0'

with open('{}/databases/movies.json'.format("."), 'r') as jsf:
   movies = json.load(jsf)
# root message
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>",200)

@app.route("/template", methods=['GET'])
def template():
    return make_response(render_template('index.html', body_text='This is my HTML template for Movie service'),200)

# Route that returns the entire movies dataset in JSON format
@app.route("/json", methods=['GET'])
def get_json():
    res = make_response(jsonify(movies), 200)
    return res

# Route to get a specific movie by its ID
@app.route("/movies/<movieid>", methods=['GET'])
def get_movie_byid(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            res = make_response(jsonify(movie),200)
            return res
    return make_response(jsonify({"error":"Movie ID not found"}),400)

# Route to get a movie by its title via query parameters
@app.route("/moviesbytitle", methods=['GET'])
def get_movie_bytitle():
    json = ""
    if request.args:
        req = request.args
        for movie in movies:
            if str(movie["title"]) == str(req["title"]):
                json = movie

    if not json:
        res = make_response(jsonify({"error":"movie title not found"}),400)
    else:
        res = make_response(jsonify(json),200)
    return res

# Route to get movies by director's name
@app.route("/moviesbydirector", methods=['GET'])
def get_movie_bydirector():
    if request.args:
        req = request.args
        director_movies = [movie for movie in movies if movie["director"] == req["director"]]
        if director_movies:
            res = make_response(jsonify(director_movies), 200)
            return res
    res = make_response(jsonify({"error": "No movies found for this director"}), 404)
    return res

# Route to filter movies by their rating
@app.route("/moviesbyrating/<rating>", methods=['GET'])
def get_movies_by_rating(rating):
    filtered_movies = [movie for movie in movies if float(movie["rating"]) == float(rating)]
    
    if not filtered_movies:
        res = make_response(jsonify({"error": "No movies found with rating {}".format(rating)}), 400)
        return res
    
    res = make_response(jsonify(filtered_movies), 200)
    return res

# Route to filter movies within a range of ratings
@app.route("/moviesbyratingrange/<min_rating>/<max_rating>", methods=['GET'])
def get_movies_by_rating_range(min_rating, max_rating):
    try:
        min_rating = float(min_rating)
        max_rating = float(max_rating)
    except ValueError:
        res = make_response(jsonify({"error": "Invalid rating values"}), 400)
        return res

    filtered_movies = [movie for movie in movies if min_rating <= movie["rating"] <= max_rating]

    if not filtered_movies:
        res = make_response(jsonify({"error": "Invalid rating values"}), 400)
        return res

    res = make_response(jsonify(filtered_movies), 200)
    return res

# Route to add a new movie 
@app.route("/addmovie/<movieid>", methods=['POST'])
def add_movie(movieid):
    req = request.get_json()

    for movie in movies:
        if str(movie["id"]) == str(movieid):
            return make_response(jsonify({"error":"movie ID already exists"}),409)

    movies.append(req)
    write(movies)
    res = make_response(jsonify({"message":"movie added"}),200)
    return res

def write(movies):
    with open('{}/databases/movies.json'.format("."), 'w') as f:
        json.dump(movies, f)

# Route to update the rating of a movie by its ID via a PUT request  
@app.route("/movies/<movieid>/<rate>", methods=['PUT'])
def update_movie_rating(movieid, rate):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movie["rating"] = rate
            res = make_response(jsonify(movie),200)
            return res

    res = make_response(jsonify({"error":"movie ID not found"}),201)
    return res

# Route to provide a list of available API endpoints and their descriptions
@app.route("/help", methods=['GET'])
def help():
    endpoints = {
        "/": "Root message",
        "/template": "Displays a simple HTML template",
        "/json": "Returns the list of movies in JSON format",
        "/movies/<movieid>": "Get movie details by movie ID",
        "/moviesbytitle": "Get movie details by movie title",
        "/moviesbydirector": "Get movies by director name",
        "/moviesbyrating": "Get movies by rating score",
        "/moviesbyratingrange/<min_rating>/<max_rating>": "Get movies within rating range [<min_rating>,<max_rating>]",
        "/addmovie/<movieid>": "Add a new movie to the database",
        "/movies/<movieid>/<rate>": "Update the rating of a movie"
    }
    return make_response(jsonify(endpoints), 200)

if __name__ == "__main__":
    #p = sys.argv[1]
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)
