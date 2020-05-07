# Full Stack API Final Project

## Casting Agency API

This project is an API designed for a casting agency that needs to control both movies and actors. App is hosted on https://capstone-agency.herokuapp.com/

There are 3 level of roles designed for this project:
	- Casting Assistant
		Can view actors and movies
	- Casting Director
		All permissions a Casting Assistant has and…
		Add or delete an actor from the database
		Modify actors or movies
	- Executive Producer
		All permissions a Casting Director has and…
		Add or delete a movie from the database

Users of the API must register through Auth0.com where the admin will assign roles for API use.

## Login

No login page has been built yet. Refer to: https://fsnd-auth-mesangue.auth0.com/authorize?audience=agency-api&response_type=token&client_id=Mv9lTQF3zroRxSWPwGXDzq4kx1AfiYdZ&redirect_uri=https://capstone-agency.herokuapp.com/

## Database Tables
	Relevant attributes for users:
	- Actors: Name (string, mandatory), age (int), gender (string), movies (array of strings)
	- Movies: Title (string, mandatory), release_date (MM/DD/YYYY), actors (array of strings)

## API functions

	URL 'https://capstone-agency.herokuapp.com/' ; Allowed method: GET ; Required Permissions: None
		returns {
			'message':'Hello World - The API is up!'
			,'success': True
			}

	URL 'https://capstone-agency.herokuapp.com/movies' ; Allowed method: GET ; Required Permissions: None
		returns JSON {
			'success' : True
			,'movies': List of movies on Database 
			}

	URL 'https://capstone-agency.herokuapp.com/movies/<int:movie_id>' ; Allowed method: GET ; Required Permissions: None
		returns JSON {
			'success' : True
			,'movies': Specific movie from Database
			}

	URL 'https://capstone-agency.herokuapp.com/actors' ; Allowed method: GET ; Required Permissions: None
		returns JSON {
			'success' : True
			,'actors': List of actors on Database
			}

	URL 'https://capstone-agency.herokuapp.com/actors/<int:actor_id>' ; Allowed method: GET ; Required Permissions: None
		returns JSON {
			'success' : True
			,'actors': Specific actor from Database
			}

	URL 'https://capstone-agency.herokuapp.com/movies/<int:movie_id>'' ; Allowed method: DELETE ; Required Permissions: None
		returns JSON {
			'success':True
			,'previous_data': Data from deleted movie
			,'deleted_id':Id of deleted movie
			}

	URL 'https://capstone-agency.herokuapp.com/actors/<int:actor_id>' ; Allowed method: DELETE ; Required Permissions: None
		returns JSON {
			'success':True
			,'previous_data': Data from deleted actor
			,'deleted_id': Id of deleted actor
			}

	URL 'https://capstone-agency.herokuapp.com/movies' ; Allowed method: POST ; Required Permissions: None
		returns JSON {
			'success':True
			,'data': Data fom new movie added to database
		}

	URL 'https://capstone-agency.herokuapp.com/actors' ; Allowed method: POST ; Required Permissions: None
		returns JSON {
			'success':True
			,'data': Data fom new actor added to database
		}

	URL 'https://capstone-agency.herokuapp.com/actors/<int:actor_id>' ; Allowed method: PATCH ; Required Permissions: None
		returns JSON {
			'success':True
			,'previous_data': Data before changes
			,'data':Updated actor data
			}

	URL 'https://capstone-agency.herokuapp.com/movies/<int:movie_id>' ; Allowed method: PATCH ; Required Permissions: None
		returns JSON {
			'success':True
			,'previous_data': Data before changes
			,'data': Updated movie data
			}





## Error messages
	All errors follow the following structure. Refer to message for troubleshooting.
						{
						"success": False, 
						"error": Status code,
						"message": Description of error (e.g. "Token expired.")
						}





