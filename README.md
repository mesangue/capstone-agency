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

    URL 'https://capstone-agency.herokuapp.com/' ; Allowed method: GET ; Required Permissions: No
        returns {
            'message':'Hello World - The API is up!'
            ,'success': True
            }

    URL 'https://capstone-agency.herokuapp.com/movies' ; Allowed method: GET ; Required Permissions: Yes
        returns JSON {
            'success' : True
            ,'movies': [{'id':1,'title':'Title','release_date':MM/DD/YYYY,'actors':['A','B']},{'id':2,'title':'Title','release_date':MM/DD/YYYY,'actors':['A','B']}]
            }

    URL 'https://capstone-agency.herokuapp.com/movies/<int:movie_id>' ; Allowed method: GET ; Required Permissions: Yes
        returns JSON {
            'success' : True
            ,'movies': {'id':1,'title':'Title','release_date':MM/DD/YYYY,'actors':['A','B']}}
            }

    URL 'https://capstone-agency.herokuapp.com/actors' ; Allowed method: GET ; Required Permissions: Yes
        returns JSON {
            'success' : True
            ,'actors': [{'id':1,'name':'Name','age':25,'gender':'X','movies':['A','B']}},{'id':2,'name':'Name','age':25,'gender':'Y','movies':['A','B']}}]
            }

    URL 'https://capstone-agency.herokuapp.com/actors/<int:actor_id>' ; Allowed method: GET ; Required Permissions: Yes
        returns JSON {
            'success' : True
            ,'actors': {'id':1,'name':'Name','age':25,'gender':'X','movies':['A','B']}
            }

    URL 'https://capstone-agency.herokuapp.com/movies/<int:movie_id>'' ; Allowed method: DELETE ; Required Permissions: Yes
        returns JSON {
            'success':True
            ,'previous_data': {'id':1,'title':'Title','release_date':MM/DD/YYYY,'actors':['A','B']}}
            ,'deleted_id': 1
            }

    URL 'https://capstone-agency.herokuapp.com/actors/<int:actor_id>' ; Allowed method: DELETE ; Required Permissions: Yes
        returns JSON {
            'success':True
            ,'previous_data': {'id':1,'name':'Name','age':25,'gender':'X','movies':['A','B']}
            ,'deleted_id': 1
            }

    URL 'https://capstone-agency.herokuapp.com/movies' ; Allowed method: POST ; Required Permissions: Yes
        returns JSON {
            'success':True
            ,'data': {'id':1,'title':'Title','release_date':MM/DD/YYYY,'actors':['A','B']}}
        }

    URL 'https://capstone-agency.herokuapp.com/actors' ; Allowed method: POST ; Required Permissions: Yes
        returns JSON {
            'success':True
            ,'data': {'id':1,'name':'Name','age':25,'gender':'X','movies':['A','B']}
        }

    URL 'https://capstone-agency.herokuapp.com/actors/<int:actor_id>' ; Allowed method: PATCH ; Required Permissions: Yes
        returns JSON {
            'success':True
            ,'previous_data': {'id':1,'name':'Name','age':25,'gender':'X','movies':['A','B']}
            ,'data': {'id':1,'name':'Name','age':25,'gender':'X','movies':['A','B']}
            }

    URL 'https://capstone-agency.herokuapp.com/movies/<int:movie_id>' ; Allowed method: PATCH ; Required Permissions: Yes
        returns JSON {
            'success':True
            ,'previous_data': {'id':1,'title':'Title','release_date':MM/DD/YYYY,'actors':['A','B']}}
            ,'data': {'id':1,'title':'Title','release_date':MM/DD/YYYY,'actors':['A','B']}}
            }





## Error messages
    All errors follow the following structure. Refer to message for troubleshooting.
        returns JSON {
            "success": False, 
            "error": 401,
            "message": "Token expired."
            }





