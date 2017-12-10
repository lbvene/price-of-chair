from app import app

__author__ = 'lbvene'

app.run(debug=app.config['DEBUG'], port=4050)
