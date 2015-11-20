import os, json
from flask import Flask, render_template, send_from_directory
from flask import url_for, request, session, redirect
from flask_oauth import OAuth

#----------------------------------------
# initialization
#----------------------------------------

app = Flask(__name__)

app.config.update(
    DEBUG = True,
)

#----------------------------------------
# controllers
#----------------------------------------

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'ico/favicon.ico')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/")
def index():
    return render_template('index.html')

#----------------------------------------
# facebook authentication
#----------------------------------------


FACEBOOK_APP_ID = 'XXXXXXXXXXXXXXXXX' 
FACEBOOK_APP_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXX'

app.config["SECRET_KEY"] = FACEBOOK_APP_SECRET

oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': ('email, ')}
)

@facebook.tokengetter
def get_facebook_token():
    return session.get('facebook_token')

@app.route("/facebook_login")
def facebook_login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next'), _external=True))

@app.route("/facebook_authorized")
@facebook.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None or 'access_token' not in resp:
        return redirect(next_url)

    session['logged_in'] = True
    session['facebook_token'] = (resp['access_token'], '')

    return redirect(next_url)

def pop_login_session():
    session.pop('logged_in', None)
    session.pop('facebook_token', None)

@app.route("/logout")
def logout():
    pop_login_session()
    return redirect(url_for('index'))

@app.route("/aboutme")
def test():
    data = facebook.get('/me').data
    if 'id' in data and 'name' in data:
        user_id = data['id']
        user_name = data['name']
    return json.dumps([user_id, user_name])

@app.route("/friends")
def friends():
    data = facebook.get('/me').data
    if 'id' in data and 'name' in data:
        user_id = data['id']
        user_name = data['name']
        data = facebook.get('/{0}/friends'.format(user_id)).data
        print data
        return json.dumps(data)
    return "Nothing found!"

#----------------------------------------
# launch
#----------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
