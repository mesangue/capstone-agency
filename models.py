import os
from sqlalchemy import Column, String, Integer, Date, CheckConstraint
from flask_sqlalchemy import SQLAlchemy
import json
from flask_migrate import Migrate #for local run test

db = SQLAlchemy()

def setup_db(app):
	app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['DATABASE_URL']
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
	db.app = app
	db.init_app(app)
	migrate = Migrate(app,db) # For local run tests
	#db.create_all() # For local run tests

class Movie(db.Model):
	__tablename__ = 'Movie'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String, nullable=False) #no limit to names
	release_date = db.Column(db.Date)
	actors = db.Column(db.ARRAY(db.String)) # One movie can have multiple actors.
	def format(self):
		return {
			'id': self.id
			,'title': self.title
			,'release_date': self.release_date
			}

	def insert(self):
		db.session.add(self)
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()

	def update(self):
		db.session.commit()	


class Actor(db.Model):
	__tablename__ = 'Actor'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	age = db.Column(db.Integer, CheckConstraint('age>0'))
	gender = db.Column(db.String) #Note: to be discussed with project owner if gender should be limited to a set of values for a data integrity purpose
	movies = db.Column(db.ARRAY(db.String)) # One actor can have multiple movies, them not even necessarily within the agency DB (e.g. famous actor never casted by this company).
	def format(self):
		return {
			'id': self.id
			,'name': self.name
			,'age': self.age
			,'gender': self.gender
			}

	def insert(self):
		db.session.add(self)
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()

	def update(self):
		db.session.commit()