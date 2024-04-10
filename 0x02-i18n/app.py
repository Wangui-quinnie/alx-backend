from flask import Flask, render_template, g
from flask_babel import Babel, _

app = Flask(__name__)
babel = Babel(app)

# Define the user table (mocked)
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

# Define the get_user function


def get_user(user_id):
    return users.get(int(user_id))

# Define the before_request function


@app.before_request
def before_request():
    user_id = request.args.get('login_as')
    g.user = get_user(user_id) if user_id else None

# Define the get_locale function


@babel.localeselector
def get_locale():
    if 'locale' in request.args:
        return request.args['locale']
    elif g.user and g.user['locale']:
        return g.user['locale']
    elif request.accept_languages.best_match(app.config['LANGUAGES']):
        return request.accept_languages.best_match(app.config['LANGUAGES'])
    return app.config['BABEL_DEFAULT_LOCALE']

# Define the get_timezone function


@babel.timezoneselector
def get_timezone():
    if 'timezone' in request.args:
        try:
            pytz.timezone(request.args['timezone'])
            return request.args['timezone']
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    elif g.user and g.user['timezone']:
        try:
            pytz.timezone(g.user['timezone'])
            return g.user['timezone']
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    return 'UTC'

# Define the index route


@app.route('/')
def index():
    # Get the current time in the selected time zone
    current_time = datetime.now(pytz.timezone(
        g.timezone)).strftime('%b %d, %Y, %I:%M:%S %p')

    # Translate the message for the current time
    current_time_message = _('current_time_is', current_time=current_time)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
