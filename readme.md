# My Weather App

Allows the user to look up weather information for any location.  The information provided is:

* Name of the location
* Date and Time at the location
* Current temperature as well as the daily high and low temperatures.  All are provided in both Fahrenheit and Celsius.
* Current weather provided both graphical and textually.

The user can save locations for easier lookups in the future.  All that is required is a single cookie; no username or password to remember.

Weather information is cached for at most 15 minutes.

## Technologies Used

* Backend
	* Django 1.6
	* Python Requests 2.1.0
	* Firebase - SaaS provided JSON database
	* ForecastIO API feed
* Frontend
	* jQuery 1.10
	* jQuery BlockUI 2.66
	* Facebook React 0.9
	* Moment 2.5.1 JS time library
	
## How To Run

All the services are cloud hosted so it's a simple matter of:

$ git clone

$ cd tsace

$ pip install -r requirements.txt

$ manage.py runserver

and browse to http://127.0.0.1:8000