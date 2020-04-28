Monolith example
=======

This code is an evolution from the Monolith. It is a Django application (https://www.djangoproject.com/) that creates a website for candidates management. It connects to both the users backend and the candidates backend.

Set it up
------

Use docker-compose to build the service

    $ docker-compose build

Configure the `environment.env` file to point to the users and candidates backend.


Up the service

    $ docker-compose up


Test and login
------

There are a couple of users created in the system, `agustina`, `ariel`, `cristian`, `fabricio` and `mariano`, password and user names are the same.

You can log in as any of them, add more candidates, and search for all the candidates in the system. No need to be logged to search.

Dependencies
------

MyCandidates uses Django as a web framework, Bootstrap for the styling and bcrypt for checking the passwords. Please note that the way of handling authentication is not safe and shouldn't be used in a production website.
