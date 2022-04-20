# Instructions for installing and running the project:

1- Install requiraments in the requirements.txt file:

```
pip install -r requirements.txt
```

2- Set the enviroment variable ALERTUS_CREDENTIALS in a file called .env:

```
ALERTUS_CREDENTIALS=<base64 encoding of <your_username>:<your_password>>
```

3- Run Flask server

```
flask run --port 8000
```

4- Run Tests

```
pytest
```

### Github Link:

https://github.com/iamrdr97

### Explaning Challenges and Highlights:

One of the biggest challenges I faced doing this project was implementing the user interface, since I had never used
technologies like jinja2 or bootstrap, and it had been a long time since I used JavaScript and jQuery.

Another important challenge was accessing weather.gov and alertus services through their APIs, but using their
documentation allowed me to achieve my goal.

What I am most proud of is having completed the project in the established time, despite the fact that to do, so I used
tools and frameworks that I do not usually use, such as flask and the ones mentioned above for the user interface.

### List of relevant libraries used:

#### requests:

**requests** allows to send HTTP requests in an easy way

#### requests-cache:

**requests-cache** is a persistent cache that provides an easy way to get better performance with the python requests
library.

#### pytest:

**pytest** is a testing framework that allows to test the code in a simple way.
