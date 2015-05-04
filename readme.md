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
	* Django 1.8.1
	* Python Requests 2.6.2
	* Firebase - SaaS provided JSON database
	* ForecastIO API feed
* Frontend
	* jQuery 2.1.4
	* jQuery BlockUI 2.66
	* Facebook React 0.13.2
	* Moment 2.5.1 JS time library
	
## How To Run

All the services are cloud hosted so it's a simple matter of:

```
$ git clone
$ cd tsace
$ pip install -r requirements.txt
$ manage.py runserver
```

and browse to http://127.0.0.1:8000

## Caveats

Because this is a small and contrived project, some shortcuts were taken 
that wouldn't normally be used in a production application.

1. None of the files are minimized/pre-compiled.  This is for ease of showing off work and critiquing.  As a result of this, the site will load slower than normally.
2. All the React code is in one file: weather-react.js.  In an actual production application, the application would be broken out into logical files and something like webpack would pull everything together.  I didn't use such a utility for this project to keep the friction as low as possible for testing it out.
3. Libraries and framework are being pulled from CDNs instead of being local assests that are bundled together.  Same reasoning as #2.