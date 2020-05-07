import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError, requires_auth
from models import setup_db, Movie, Actor

def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)
    setup_db(app)

    @app.route('/') 
    def greeting(): 
        return jsonify({
            'message': 'Hello World - The API is up!'
            , 'success':  True
        })

    @app.route('/movies', methods=['GET']) 
    @requires_auth('get: movies')
    def get_movies(jwt):
        movies = Movie.query.all()
        if len(movies) == 0: 
            abort(404)
        movie_list = [item.format() for item in movies]
        return jsonify({
            'success':  True
            , 'movies':  movie_list
        })

    @app.route('/movies/<int: movie_id>', methods=['GET']) 
    @requires_auth('get: movies')
    def get_single_movie(jwt,movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None: 
            abort(404)
        return jsonify({
            'success':  True
            , 'movies':  [movie.format()]
        })

    @app.route('/actors', methods=['GET']) 
    @requires_auth('get: actors')
    def get_actors(jwt):
        actors = Actor.query.all()
        if len(actors) == 0: 
            abort(404)
        actor_list = [item.format() for item in actors]
        return jsonify({
            'success':  True
            , 'actors':  actor_list
        })

    @app.route('/actors/<int: actor_id>', methods=['GET']) 
    @requires_auth('get: actors')
    def get_single_actor(jwt,actor_id):
        actor = Movie.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None: 
            abort(404)
        return jsonify({
            'success':  True
            , 'actors':  [actor.format()]
        })

    @app.route('/movies/<int: movie_id>', methods=['DELETE'])
    @requires_auth('delete: movies')
    def delete_movie(jwt,movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None: 
            abort(404)
        old_data = movie.format()
        try: 
            movie.delete()
            return jsonify({
                'success': True
                , 'previous_data': old_data
                , 'deleted_id': movie_id
            })
        except: 
            abort(422)

    @app.route('/actors/<int: actor_id>', methods=['DELETE'])
    @requires_auth('delete: actors')
    def delete_actor(jwt,actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None: 
            abort(404)
        old_data = actor.format()
        try: 
            actor.delete()
            return jsonify({
                'success': True
                , 'previous_data': old_data
                , 'deleted_id': actor_id
            })
        except: 
            abort(422)

    @app.route('/movies', methods=['POST']) 
    @requires_auth('post: movies')
    def add_movie(jwt):
        data = request.get_json()
        if data is None or len(str(data['title']).strip())==0: 
            abort(400)
        try: 
            new_movie = Movie(
                title = str(data['title'])
                ,release_date = data['release_date']
                )
            new_movie.insert()
            return jsonify({
                'success': True
                , 'data':  new_movie.format()
            })
        except: 
            abort(422)

    @app.route('/actors', methods=['POST']) 
    @requires_auth('post: actors')
    def add_actor(jwt):
        data = request.get_json()
        if len(str(data['name']).strip())==0 or data is None: # will allow gender to be anything - TBD by project owner
            abort(400)
        try: 
            if int(data['age'])<=0: 
                abort(400)
        except: 
            abort(400)
        try: 
            new_actor = Actor(
                name = str(data['name'])
                ,age = data['age']
                ,gender = str(data['gender'])
            )
            new_actor.insert()
            return jsonify({
                'success': True
                , 'data':  new_actor.format()
            })
        except: 
            abort(422)

    @app.route('/actors/<int: actor_id>', methods=['PATCH']) 
    @requires_auth('patch: actors')
    def patch_actors(jwt,actor_id):
        data = request.get_json()
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if data is None: 
            abort(404)
        old_data = actor.format()
        if 'name' in data: 
            if len(str(data['name']).strip())==0: 
                abort(400)
            actor.name = data['name']
        if 'age' in data: 
            try: 
                if int(data['age'])<=0: 
                    abort(400)
            except: 
                abort(400)
            actor.age = data['age']
        if 'gender' in data: 
            actor.gender = data['gender']
        try: 
            actor.update()
            return jsonify({
                'success': True
                , 'previous_data': old_data
                , 'data': [actor.format()]
            })
        except: 
            abort(422)

    @app.route('/movies/<int: movie_id>', methods=['PATCH']) 
    @requires_auth('patch: movies')
    def patch_movies(jwt,movie_id):
        data = request.get_json()
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None: 
            abort(404)
        old_data = movie.format()
        if 'title' in data: 
            if len(str(data['title']).strip())==0: 
                abort(400)
            else: 
                movie.title = data['title']
        if 'release_date' in data: 
            movie.release_date = data['release_date']
        try: 
            movie.update()
            return jsonify({
                'success': True
                , 'previous_data': old_data
                , 'data': [movie.format()]
            })
        except: 
            abort(422)

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success":  False, 
            "error":  422,
            "message":  "unprocessable"
        }), 422

    @app.errorhandler(404)
    def notfound(error):
        return jsonify({
            "success":  False, 
            "error":  404,
            "message":  "not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False
            , 'error': 400
            , 'message':  'bad request'
        }), 400

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False
            , 'error': 500
            , 'message':  'internal server error'
        }), 500

    @app.errorhandler(AuthError)
    def autherror(AuthError):
        return jsonify({
            "success":  False, 
            "error":  AuthError.status_code,
            "message":  AuthError.error['description']
        }), AuthError.status_code

    return app

app = create_app()

if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=8080, debug=True)
