import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth


class CapstoneTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app)


        self.assistant_header = {
            'Authorization': 'Bearer {}'.format(os.environ.get('ASSISTANT_TOKEN'))
        }
        self.director_header = {
            'Authorization': 'Bearer {}'.format(os.environ.get('DIRECTOR_TOKEN'))
        }
        self.producer_header = {
            'Authorization': 'Bearer {}'.format(os.environ.get('PRODUCER_TOKEN'))
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_movie = {
            'title': 'Designated Survivor',
            'release_date': '2018-02-01'
        }

        self.new_actor = {
            'name': 'DiCaprio',
            'age': 24,
            'gender': 'Male'
        }
    
    def tearDown(self):
        """Executed after reach test"""

    def testGetActorsSuccess(self):
        res = self.client().get('/actors',headers=self.assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def testGetActorsFailure(self):
        res = self.client().get('/actorrrs')
        self.assertEqual(res.status_code, 404)

    def testGetMoviesSuccess(self):
        res = self.client().get('/movies',headers=self.assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def testGetMoviesFailure(self):
        res = self.client().get('/moviess')
        self.assertEqual(res.status_code, 404)

    def testPostActorSuccess(self):
        res = self.client().post('/actors', json=self.new_actor,
                                 headers=self.director_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'],'Successfully added actor')

    def testPostActorFailure(self):
        res = self.client().post('/actorsss', json=self.new_actor)
        self.assertEqual(res.status_code, 404)

    def testPostMovieSuccess(self):
        res = self.client().post('/movies', json=self.new_movie,
                                 headers=self.producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'],'Successfully added movie')

    def testPostMovieAccessFailure(self):
        res = self.client().post('/movies', json=self.new_movie,
                                 headers=self.assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def testPostMoviesFailure(self):
        res = self.client().post('/moviess', json=self.new_movie)
        self.assertEqual(res.status_code, 404)

    def testPatchActorSuccess(self):
        res = self.client().patch('/actors/update/1', json=self.new_actor,
                                 headers=self.director_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'],'Successfully updated actor')

    def testPatchActorFailure(self):
        res = self.client().patch('/actorsss/update/1', json=self.new_actor)
        self.assertEqual(res.status_code, 404)
"""
    def testPatchMovieSuccess(self):
        res = self.client().patch('/movies/update/1', json=self.new_movie,
                                 headers=self.director_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'],'Successfully updated movie')
"""
    def testPatchMoviesFailure(self):
        res = self.client().patch('/moviesss/update/1', json=self.new_movie)
        self.assertEqual(res.status_code, 404)

    def testDeleteActorSuccess(self):
        res = self.client().delete('/actors/delete/1', headers=self.director_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'],'Successfully deleted actor')

    def testDeleteActorFailure(self):
        res = self.client().delete('/actorsss/delete/1')
        self.assertEqual(res.status_code, 404)

    def testDeleteMovieSuccess(self):
        res = self.client().delete('/movies/delete/1', headers=self.producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'],'Successfully deleted movie')

    def testDeleteMovieFailure(self):
        res = self.client().delete('/moviessss/delete/1')
        self.assertEqual(res.status_code, 404)
"""

if __name__ == "__main__":
    unittest.main()
