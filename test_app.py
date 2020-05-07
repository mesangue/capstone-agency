import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth

class CapstoneTestCase(unittest.TestCase):
	def setUp(self):
		self.app = create_app()
		self.client = self.app.test_client
		self.header_assistant = {'Content-Type': 'application/json', 'Authorization': 'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRXTmJXbzVwZ2pod2dPUHlNWnQtWiJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYXV0aC1tZXNhbmd1ZS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU5ZjY5M2MzOWQ5NDYwY2EwOGVhNGQzIiwiYXVkIjoiYWdlbmN5LWFwaSIsImlhdCI6MTU4ODgyODU2MiwiZXhwIjoxNTg4OTE0OTYyLCJhenAiOiJNdjlsVFFGM3pyb1J4U1dQd0dYRHpxNGt4MUFmaVlkWiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.JQaHJu08Rxr_I2eX5pZSJapF3Z3NweN7mFyjaEpJ_nHw9f2eFWgoDorPWp4h8iXn45NRJU9CVIW0_pnwwaQjI1pifzqr7XycUOp2aUZv2TTG-L2SZ4X_P0gCFJ1dW47sDzY0OdJoLyYrQM0ETmEN1i90cQCihtxW28utPTIm8vLU-7_DLUCj--_sz24CPskeCBLM2VI1pn6iSiroBqxe0pS2I4fRWJBxfcr6CFahhtup-D5lvZW84G4XG2ZgUOvXdRS1k_2g381gPJgaMwJbgJeBI66Dmez_cTyY3N8MSeAMH_SwLfrgbUXT7h1u-dIpUAbN4CB42TcEP-YWrE_d9w'}
		# get actors, get movies
		self.header_director = {'Content-Type': 'application/json', 'Authorization': 'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRXTmJXbzVwZ2pod2dPUHlNWnQtWiJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYXV0aC1tZXNhbmd1ZS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU5ZjZhMjgyMDdmMzQwYzkwMTI5MzU1IiwiYXVkIjoiYWdlbmN5LWFwaSIsImlhdCI6MTU4ODgyODYxOSwiZXhwIjoxNTg4OTE1MDE5LCJhenAiOiJNdjlsVFFGM3pyb1J4U1dQd0dYRHpxNGt4MUFmaVlkWiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.n67oGbmeT5aAl_um74vBmDBCRMeufnOsCv8Ob6VXRxda2BAzLahMehil0HSjIJa_UduRq75L-fBtXRGEm9_dzkuAo5OnyuIwjNihnXyOKfw_hQLKgsktJoDywuSUBVnNjh1bVu6Xj5jIWAUycmtIaqzF4Wk3DU9BKRdeqAN8tJOWScaJaHaklQGna7197RSTUj5Xs6OeHqDiRswXbd1z7lb7PN6NIQkKNF6OH5UcF8QEC_VP2P-IB9XRlH4bL6iHzkmqCIcaTZ2yNuH-2VsQFRDPL7MTJ3b47g2ESwWhtdw8aSxNRzJ4fHorkcijZfq0-S6IxSTsZBaEvxFhNMXrWQ'}
		# delete actors, patch actors
		self.header_producer = {'Content-Type': 'application/json', 'Authorization': 'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRXTmJXbzVwZ2pod2dPUHlNWnQtWiJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYXV0aC1tZXNhbmd1ZS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViMGQ4MjM1NGIxNGMwYzEyNzc1OTc2IiwiYXVkIjoiYWdlbmN5LWFwaSIsImlhdCI6MTU4ODgyOTQ1MywiZXhwIjoxNTg4OTE1ODUzLCJhenAiOiJNdjlsVFFGM3pyb1J4U1dQd0dYRHpxNGt4MUFmaVlkWiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.Mirx_mBsmiGEHByH5PEUV9hl09iFGingbzel8eTYn-LMQnWwvBbFlNpefgsOZ1Bxc9aFhZwGSikTIo3TWMrlT5ONhirDfef0oSH0QmLtJsfYtwq0O8ZfEqj1h-H8523n34vkb2dVCbsB9gS_5MlkCj4LbINn1xsggP4zENVFUAAUUsxW4EctEykwUMcqi0P6EsJBtqmiQ94x5UonFjkHsq6_vi2rg8aJ-RzhYB0vz1dDDai3jIQpmDXh9jwAiOyqz-Moz2b_5uJlQe80V90CeoVcKjJsCfC46bSsXxV65d7bTxu8PM36IJ3pmfOBZ5f96Pb8EoZKdrWLvWs8IkKuug'}
		# all else
		setup_db(self.app)
		self.sample_movie = {
			'title' : 'Diehard'
			, 'release_date': '07/15/1988'
		}

		self.sample_actor = {
			'name': 'Bruce Willis'
			, 'age': '32'
			, 'gender': 'male'
		}
		
		with self.app.app_context():
			self.db = SQLAlchemy()
			self.db.init_app(self.app)
			self.db.create_all()
	
	def tearDown(self):
		pass

	def test_app_setup(self):
		res = self.client().get('/')
		data = json.loads(res.data)
		self.assertEqual(res.status_code,200)
		self.assertEqual(data['success'],True)


	def test_post_actor(self):
		res = self.client().post('/actors',json=self.sample_actor, headers=self.header_producer)
		data = json.loads(res.data)
		self.assertEqual(res.status_code,200)
		self.assertEqual(data['success'],True)
		self.assertEqual(data['data']['name'], 'Bruce Willis')

	def test_failed_post_actor(self):
		res = self.client().post('/actors', headers=self.header_producer) # no json for creation
		data = json.loads(res.data)
		self.assertEqual(res.status_code,400)
		self.assertEqual(data['success'],False)
		self.assertEqual(data['message'], 'bad request')

	def test_get_actors(self):
		res = self.client().get('/actors', headers=self.header_assistant)
		data = json.loads(res.data)
		self.assertEqual(res.status_code,200)
		self.assertEqual(data['success'],True)

	def test_patch_actor(self):
		sample = Actor.query.first()
		res = self.client().patch('/actors/'+str(sample.id),json={'name': 'Walter Bruce Willis'}, headers=self.header_director)
		data = json.loads(res.data)
		old_data = self.sample_actor
		self.assertEqual(res.status_code,200)
		self.assertEqual(data['success'],True)

	def test_failed_patch_actor(self):
		sample = Actor.query.first()
		res = self.client().patch('/actors/'+str(sample.id), headers=self.header_director) # no name
		data = json.loads(res.data)
		self.assertEqual(res.status_code,400)
		self.assertEqual(data['success'],False)
		self.assertEqual(data['message'], 'bad request')

	def test_succesful_delete_actor(self):
		sample = Actor.query.first() #delete first result for test
		res = self.client().delete('/actors/'+str(sample.id), headers=self.header_director)
		data = json.loads(res.data)
		actor = Actor.query.filter(Actor.id == sample.id).one_or_none() #1 per id, or none
		self.assertEqual(res.status_code,200)
		self.assertEqual(data['success'],True)
		self.assertEqual(data['deleted_id'],sample.id)
		self.assertEqual(actor,None) # object was deleted

	def test_failed_delete_actor(self):
		res = self.client().delete('/actors/9999999999', headers=self.header_producer) # no such actor
		data = json.loads(res.data)
		self.assertEqual(res.status_code,404)
		self.assertEqual(data['success'],False)
		self.assertEqual(data['message'], 'not found')

	def test_post_movie(self):
		res = self.client().post('/movies',json=self.sample_movie, headers=self.header_producer)
		data = json.loads(res.data)
		self.assertEqual(res.status_code,200)
		self.assertEqual(data['success'],True)
		self.assertEqual(data['data']['title'], 'Diehard')

	def test_failed_post_movie(self):
		res = self.client().post('/movies', headers=self.header_producer) # no json for creation
		data = json.loads(res.data)
		self.assertEqual(res.status_code,400)
		self.assertEqual(data['success'],False)
		self.assertEqual(data['message'], 'bad request')

	def test_get_movies(self):
		res = self.client().get('/movies', headers=self.header_assistant)
		data = json.loads(res.data)
		self.assertEqual(res.status_code,200)
		self.assertEqual(data['success'],True)

	def test_patch_movie(self):
		sample = Movie.query.first()
		res = self.client().patch('/movies/'+str(sample.id),json={'name': 'Diehard.'}, headers=self.header_producer)
		old_data = self.sample_movie
		data = json.loads(res.data)
		self.assertEqual(res.status_code,200)
		self.assertEqual(data['success'],True)

	def test_failed_patch_movie(self):
		sample = Movie.query.first()
		res = self.client().patch('/movies/'+str(sample.id), headers=self.header_producer) # no title
		data = json.loads(res.data)
		self.assertEqual(res.status_code,400)
		self.assertEqual(data['success'],False)
		self.assertEqual(data['message'], 'bad request')

	def test_succesful_delete_movie(self):
		sample = Movie.query.first() #delete first result for test
		res = self.client().delete('/movies/'+str(sample.id), headers=self.header_producer)
		data = json.loads(res.data)
		movie = Movie.query.filter(Movie.id == sample.id).one_or_none() #1 per id, or none
		self.assertEqual(res.status_code,200)
		self.assertEqual(data['success'],True)
		self.assertEqual(data['deleted_id'],sample.id)
		self.assertEqual(movie,None) # object was deleted

	def test_failed_delete_movie(self):
		res = self.client().delete('/movies/999999999999', headers=self.header_producer) # no such movie
		data = json.loads(res.data)
		self.assertEqual(res.status_code,404)
		self.assertEqual(data['success'],False)
		self.assertEqual(data['message'], 'not found')

	def test_no_jwt(self):
		sample = Actor.query.first() #delete first result for test
		res = self.client().delete('/actors/'+str(sample.id))
		data = json.loads(res.data)
		self.assertEqual(res.status_code,401)
		self.assertEqual(data['message'],"Authorization not included in JWT")

	def test_no_permissions_for_action(self):
		sample = Actor.query.first() #delete first result for test
		res = self.client().delete('/actors/'+str(sample.id), headers=self.header_assistant)
		data = json.loads(res.data)
		self.assertEqual(res.status_code,401)
		self.assertEqual(data['message'],"User does not have permission")

if __name__ == "__main__": 
    unittest.main()