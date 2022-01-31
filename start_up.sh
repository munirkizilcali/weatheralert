#! /bin/bash

# If virtualenv not installed, download & install it for user
if ! python3 -c "import virtualenv" &> /dev/null; then
    python3 -m pip install --user virtualenv
fi

# Create  virtual env for python dependencies
python3 -m virtualenv env
source env/bin/activate

# Install reqs
pip install -r requirements.txt

# Start app
python app.py
