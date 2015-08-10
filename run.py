#!flask/bin/python

from app import app

# # parser = argparse.ArgumentParser(description='Start app')
# parser.add_argument('-d', '--debug', action='store_true')
# args = parser.parse_args()
app.run(debug=True)
