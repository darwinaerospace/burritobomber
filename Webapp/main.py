#!/usr/bin/python
from flask import Flask, render_template, session, flash, request, redirect, url_for
import subprocess

app = Flask(__name__)

coordinates_email = 'example@example.com'  # Super high-tech!


def valid_code(code):
	return code == 'angelburrito'  # Super secure!


@app.route('/')
def home():
	return render_template('index.html')


@app.route('/submitcode', methods=['POST'])
def submitcode():
	code = request.form['code']

	if valid_code(code):
		session['code'] = request.form['code']
		return redirect(url_for('find_location'))
	else:
		flash('Invalid burrito code! This prototype app only allows one user at a time to request a burrito, so please wait your turn.')
		return redirect(url_for('home'))


@app.route('/find_location')
def find_location():
	return render_template('find_location.html')


@app.route('/request_burrito', methods=['POST'])
def request_burrito():
	longitude = request.form['longitude']
	latitude = request.form['latitude']

	# Hope you're running a UNIX!
	mp = subprocess.Popen(['mail', '-s', 'Burrito coordinates', coordinates_email], stdin=subprocess.PIPE)
	mp.stdin.write('%s %s' % (longitude, latitude))
	mp.stdin.write('\n')
	mp.stdin.close()
	assert mp.wait() == 0

	return redirect(url_for('burrito_requested'))


@app.route('/burrito_requested')
def burrito_requested():
	return render_template('burrito_requested.html')


app.secret_key = 'hurpadurpablurp'  # Super secret!

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
