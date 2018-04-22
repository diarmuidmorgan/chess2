import os
from app import app

def run():
	'''run the app. Access data via api,
	or view at :5000/
	or :5000/circles'''

	app.run()


if __name__ == "__main__":



	import random, threading, webbrowser

	port = 5000
	url = "http://localhost:{0}".format(port)

	

	app.run(host='0.0.0.0', port=port, debug=False)
