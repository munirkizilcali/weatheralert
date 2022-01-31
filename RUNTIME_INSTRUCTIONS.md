Note:
A few things where unclear for me in the instructions. When changing settings, should only the next calls to the api be based on the new settings, or should the whole app reflect the new settings? Currently its the ladder and all data is reset to be based on the updated settings. Also, the settings file is never actually modified, the state of the settings is just managed in memory. Additionally, the instructions name the db and the virtual environment are listed as 'deliverables'. But from my experience its quite bad practice to upload these. They will be created when running the startup script. I can upload the local copies I have if needed, just not sure that is expected or needed.


For best security practices, all credentials are managed as environment variables. So first create a .env file from the template and fill in necessary values. 
Something like: cat .env.template >> .env && vim .env


macOS & Linux
    - /bin/bash startup.sh
    or
    - make a virtual env and activate
    - install deps
    - python app.py

Windows
    - make a virtual env and activate
    - install deps
    - python app.py
