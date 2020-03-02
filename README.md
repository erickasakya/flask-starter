Monolith example
=======

This code is our example of Monolith. It is a Django application (https://www.djangoproject.com/) that creates a website for candidates management.

**THIS IS AN EXAMPLE WEBSITE**

Set it up
------

Create a virtual environment and install the requirements

    $ python3 -m venv ./venv
    $ source ./venv/bin/activate
    $ pip install -r requirements.txt


Get the local database ready and load some initial data for testing

    $ cd mycandidates/
    $ python manage.py migrate
    ...
    $ python manage.py loaddata candidates.json users.json
    Installed 7 object(s) from 2 fixture(s)

Start the development server

    $ python manage.py runserver
    Watching for file changes with StatReloader
    Performing system checks...
    
    System check identified no issues (0 silenced).
    ...
    Django version 2.2.1, using settings 'mycandidates.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

Check the service at http://127.0.0.1:8000/


Test and login
------

There are five users created in the system, `agustina`, `fabricio`, `mariano`, `cristian`,  and `ariel`, their password are "password".

You can log in as any of them, add more "candidates", and search for all the candidates in the system. No need to be logged to search.


Dependencies
------

MyCandidates uses Django as a web framework, Bootstrap for the styling and bcrypt for checking the passwords.
