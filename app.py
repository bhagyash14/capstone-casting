import os
from flask import Flask, request, jsonify, abort, render_template
from sqlalchemy import exc
import json
from flask_cors import CORS

from models import db_drop_and_create_all, setup_db, Actor, Movie
from auth import AuthError, requires_auth

AUTH0_DOMAIN = 'capstone-admin.us.auth0.com'
ALGORITHMS = ['RS256']
AUTH0_JWT_API_AUDIENCE = 'http://127.0.0.1:5000'
AUTH0_CLIENT_ID = 'QvsqXaFdw95ybQhMNelS25IaGP3OAmd5'
AUTH0_CALLBACK_URL = 'http://127.0.0.1:8100'

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    cors=CORS(app)
    #CORS(app,resources={r"/api/": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response
    #db_drop_and_create_all()

    @app.route("/authorization/url", methods=["GET"])
    def generate_auth_url():
        url = f'https://{AUTH0_DOMAIN}/authorize' \
            f'?audience={AUTH0_JWT_API_AUDIENCE}' \
            f'&response_type=token&client_id=' \
            f'{AUTH0_CLIENT_ID}&redirect_uri=' \
            f'{AUTH0_CALLBACK_URL}'
        return jsonify({
            'url': url
        })
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actor')
    def get_all_actors(token):
        all_actors = [actors.format() for actors in Actor.query.all()]
        return jsonify({
            'success': True,
            'actors': all_actors
        }),200

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movie')
    def get_all_movies(token):
        all_movies = [movies.format() for movies in Movie.query.all()]

        return jsonify({
            'success': True,
            'movies': all_movies
        }),200

    @app.route('/actors', methods=['POST'])
    @requires_auth('add:actor')
    def post_actors(payload):
        data = request.get_json()
        if 'name' and 'age' and 'gender' not in data:
            abort(422)

        actor_name = data['name']
        actor_age = data['age']
        actor_gender = data['gender']

        new_actor = Actor(name=actor_name, age=actor_age , gender=actor_gender)
        new_actor.insert()

        return jsonify({
            'success': True,
            'message':'Successfully added actor',
            'created': new_actor.id
        }),200

    @app.route('/movies', methods=['POST'])
    @requires_auth('add:movie')
    def post_movies(payload):
        data = request.get_json()
        if 'title' and 'release_date' not in data:
            abort(422)

        movie_title = data['title']
        movie_release_date = data['release_date']

        new_movie = Movie(title=movie_title, release_date=movie_release_date)
        new_movie.insert()

        return jsonify({
            'success': True,
            'message':'Successfully added movie',
            'created': new_movie.id
        }),200

    @app.route('/actors/update/<int:id>', methods=['PATCH'])
    @requires_auth('update:actor')
    def patch_actor(payload, id):
        actor = Actor.query.filter(Actor.id == id).one_or_none()
        if not actor:
            abort(404)

        data = request.get_json()
        if 'name' in data:
            actor.title = data['name']
        if 'age' in data:
            actor.age = data['age']
        if 'gender' in data:
            actor.gender = data['gender']
        actor.update()

        return jsonify({
            'success': True,
            'message':'Successfully updated actor',
            'actor': actor.id
        }),200

    @app.route('/movies/update/<int:id>', methods=['PATCH'])
    @requires_auth('update:movie')
    def patch_movie(payload, id):
        movie = Movie.query.filter(Movie.id == id).one_or_none()
        if not movie:
            abort(404)

        data = request.get_json()
        if 'title' in data:
            movie.title = data['title']
        if 'release_date' in data:
            movie.release_date = data['release_date']
        movie.update()

        return jsonify({
            'success': True,
            'message':'Successfully updated movie',
            'movie': movie.id
        }),200

    @app.route('/actors/delete/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(payload, id):

        actor = Actor.query.filter(Actor.id == id).one_or_none()
        if not actor:
            abort(404)

        actor.delete()

        return jsonify({
            'success': True,
            'message':'Successfully deleted actor',
            'delete': actor.id
        }),200

    @app.route('/movies/delete/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(payload, id):

        movie = Movie.query.filter(Movie.id == id).one_or_none()
        if not movie:
            abort(404)

        movie.delete()

        return jsonify({
            'success': True,
            'message':'Successfully deleted movie',
            'delete': movie.id
        }),200

    ## Error Handling
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                        "success": False, 
                        "error": 422,
                        "message": "unprocessable"
                        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "unauthorized"
        }), 401

    @app.errorhandler(AuthError)
    def handleAuthError(error):
        response = jsonify(error.error)
        response.status_code = error.status_code
        return response

    return app

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
