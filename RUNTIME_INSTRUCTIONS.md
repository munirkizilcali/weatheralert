## Github
[Me](https://github.com/hyptocrypto)

## Notes
I like to use an ORM when possible. This could run a tiny bit faster with raw sql executions, just not as clean or readable IMO.

A few things where unclear for me in the instructions. When changing settings, should only the next calls to the api be based on the new settings, or should the whole app reflect the new settings? Currently its the ladder and all data is reset to be based on the updated settings. Also, the settings file is never actually modified, the state of the settings is just managed in memory. Additionally, the instructions name the db and the virtual environment are listed as 'deliverables'. But from my experience its quite bad practice to upload these. They will be created when running the startup script. I can upload the local copies I have if needed, just not sure that is expected or needed.

## Security 
For best security practices, all credentials are managed as environment variables. So first create a .env file from the template and fill in necessary values. 
```bash
cat .env.template >> .env && vim .env
```
Also, of course the HTML form implements some CSRF protection. Since its just one simple form I just made it with raw HTML. For anything outside of a simple demo app like this, I would use flask-wtf forms.


## Run steps
macOS & Linux


    - /bin/bash startup.sh
    or
    - make a virtual env and activate
    - install deps
    - python app.py
 

 
Windows


    - make a virtual env and activate
    - install deps
    - python3 app.py


## Libraries
Flask: for the backed<br/>
Flask-wtf: for CSRF <br/>
PeeWee: A lightweight ORM. Cleaner and easier then a bunch of raw SQL.<br/>
Requests: For calling API's and parsing responses<br/>
Dateutil: The datetime format of the the weather api was a little weird. This made it easy to parse into a more readable format. <br/>
Dotenv: To manage env variables<br/>


## Challenge
1. Ensuring that the threaded background worker actually updated the db. Tested and it does. Please let me know if something goes wrong there, threads can be weird thanks to pythons GIL.
2. Spent a short while trying to pass the right data to one of the Alertus endpoints and kept getting 500's. I was just hitting the wrong endpoint to activate an alert.


## Extra
Using threads to speed up I/O calls to API. Also, updating the data at the set check in frequency is handled by a background thread to not block.
Code is linted with isort, flake8, and balck. Depending on flake8 config, it should pass linting tests.
