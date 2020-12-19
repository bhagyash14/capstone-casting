import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Movies, Actors
from auth import AuthError, requires_auth


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_movie = {
            'title': 'Titanic',
            'release_date': '1990'
        }

        self.new_actor = {
            'name': 'DiCaprio',
            'age': 24,
            'gender': 'Male'
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass
    def testGetActorsSuccess(self):
        res = self.client().get('/actors')
        self.assertEqual(res.status_code, 200)

    def testGetActorsFailure(self):
        res = self.client().get('/actorrrs')
        self.assertEqual(res.status_code, 404)

    def testGetMoviesSuccess(self):
        res = self.client().get('/movies')
        self.assertEqual(res.status_code, 200)

    def testGetMoviesFailure(self):
        res = self.client().get('/moviess')
        self.assertEqual(res.status_code, 404)

    def testPostActorSuccess(self):
        res = self.client().post('/actors', json=self.new_actor)
        self.assertEqual(res.status_code, 200)

    def testPostActorFailure(self):
        res = self.client().post('/actorsss', json=self.new_actor)
        self.assertEqual(res.status_code, 404)

    def testPostMovieSuccess(self):
        res = self.client().post('/movies', json=self.new_movie)
        self.assertEqual(res.status_code, 200)

    def testPostMoviesFailure(self):
        res = self.client().post('/moviess', json=self.new_movie)
        self.assertEqual(res.status_code, 404)

    def testPatchActorSuccess(self):
        res = self.client().post('/actors/update/1', json=self.new_actor)
        self.assertEqual(res.status_code, 200)

    def testPatchActorFailure(self):
        res = self.client().post('/actorsss/update/1', json=self.new_actor)
        self.assertEqual(res.status_code, 404)

    def testPatchMovieSuccess(self):
        res = self.client().post('/movies/update/1', json=self.new_movie)
        self.assertEqual(res.status_code, 200)

    def testPatchMoviesFailure(self):
        res = self.client().post('/moviesss/update/1', json=self.new_movie)
        self.assertEqual(res.status_code, 404)

    def testDeleteActorSuccess(self):
        res = self.client().post('/actors/delete/1')
        self.assertEqual(res.status_code, 200)

    def testDeleteActorFailure(self):
        res = self.client().post('/actorsss/delete/1')
        self.assertEqual(res.status_code, 404)

    def testDeleteMovieSuccess(self):
        res = self.client().post('/movies/delete/1')
        self.assertEqual(res.status_code, 200)

    def testDeleteMovieFailure(self):
        res = self.client().post('/moviessss/delete/1')
        self.assertEqual(res.status_code, 404)



if __name__ == "__main__":
    unittest.main()
