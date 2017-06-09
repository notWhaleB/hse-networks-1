from __future__ import print_function

from flask import Flask, url_for, render_template, request, session, redirect

import auth
import operations as ops

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/')
def user():
    if 'user' in session:
        return render_template('user.html', user=session['user'])
    return redirect(url_for('user_login'))


@app.route('/user/ops/cities/')
def cities():
    if 'user' not in session:
        return render_template('user.html', user=session['user'])
    return render_template('cities.html')


@app.route('/user/ops/cities/<region_id>/')
def op_cities(region_id):
    # if 'user' not in session:
    #     return render_template('user.html', user=session['user'])
    return ops.cities(region_id)


@app.route('/user/ops/factorize/<number>/')
def op_factorize(number):
    # if 'user' not in session:
    #     return render_template('user.html', user=session['user'])
    return ops.factorize(int(number))


@app.route('/user/ops/ping/')
def op_ping():
    if 'user' not in session:
        return render_template('user.html', user=session['user'])
    if 'ping' in session:
        session.pop('ping')
    ops.ping(session, request.remote_addr)
    return render_template('ping.html')


@app.route('/user/ops/ping/poll/')
def op_ping_poll():
    if 'user' not in session:
        return render_template('user.html', user=session['user'])
    if 'ping' in session:
        return ops.ping_poll(session)
    return 'There is no running ping task', 404


@app.route('/user/signup/', methods=['GET', 'POST'])
def user_signup():
    if 'user' in session:
        return redirect(url_for('user'))
    if request.method == 'POST':
        user, passwd, email = request.form['user'], request.form['passwd'], request.form['email']
        try:
            auth.do_signup(user, passwd, email)
        except auth.UserExists:
            return render_template(
                'signup.html', error='%s already exists' % user,
                user=user, passwd=passwd, email=email
            )
        return redirect(url_for('user_login'))
    else:
        return render_template('signup.html')


@app.route('/user/login/', methods=['GET', 'POST'])
def user_login():
    if 'user' in session:
        return redirect(url_for('user'))
    if request.method == 'POST':
        user, passwd = request.form['user'], request.form['passwd']
        try:
            auth.do_login(user, passwd)
            session['user'] = user
            return redirect(url_for('user'))
        except auth.BadCredentials:
            return render_template('login.html', error='Incorrect user or password', user=user)
    else:
        return render_template('login.html')


@app.route('/user/logout/')
def user_logout():
    if 'user' in session:
        session.pop('user', None)
        return redirect(url_for('user_login'))


if __name__ == '__main__':
    app.secret_key = 'CH)&*H$w07hf9wg3gAS(=1'
    app.run('0.0.0.0', 5001)
