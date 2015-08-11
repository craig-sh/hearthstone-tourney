import os
# create a file called secret_key.py in the same folder as config.py
# and declare the variable:
# secret_key = 'some-secret-key'
from secret_key import secret_key

WTF_CSRF_ENABLED = True
SECRET_KEY = secret_key

basedir = os.path.abspath(os.path.dirname(__file__))

# DB_FILE_PATH = os.path.join('/tmp', 'app.db')
DB_FILE_PATH = os.path.join(basedir, 'app.db')

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DB_FILE_PATH
