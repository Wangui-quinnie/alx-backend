#!/usr/bin/env python3
"""
3-app.py
Basic Flask app with Babel configuration
"""


from flask import Flask, render_template, request
from flask_babel import Babel, _


app = Flask(__name__)
babel = Babel(app)


class Config:
    """
    Config class for Flask app
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


@app.route('/')
def hello_world():
    """Renders the index.html template"""
    return render_template('3-index.html', title=_('home_title'), header=_('home_header'))


@babel.localeselector
def get_locale():
    """
    Determine the best matching language based on the client's request.

    Returns:
        str: The best matching language code.
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


if __name__ == "__main__":
    app.run()