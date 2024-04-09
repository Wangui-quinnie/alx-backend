#!/usr/bin/env python3
"""
1-app.py
Basic Flask app with Babel configuration
"""


from flask import Flask, render_template
from flask_babel import Babel


app = Flask(__name__)
babel = Babel(app)
app.config.from_object(Config)


class Config:
    """
    Config class for Flask app
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


@app.route('/')
def hello_world():
    """Renders the index.html template"""
    return render_template("0-index.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
