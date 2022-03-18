from . import app
# import requests
# from models import User

#
# @app.route('/')
# def home():
# 	# eew = User.query.all()
# 	q = requests.get('http://localhost:5000/api/user/1')
# 	return q.text


if __name__ == '__main__':
	app.run(debug=True)
