

from flask import Flask, abort, send_from_directory
import os
import configparser
app = Flask(__name__)

def parse_config(config_paths):
    config_path = None
    for f in config_paths:
        if os.path.isfile(f):
            config_path = f
            break

    if config_path is None:
        raise RuntimeError("Configuration file not found!")

    config = configparser.ConfigParser()
    config.read(config_path)
    return config

config = parse_config(["credentials.ini", "default.ini"])


@app.route("/<url>")
def triviahtml(url):
    if '..' in url or '~' in url:
        abort(403)
    elif url.endswith("trivia.html"):
        return send_from_directory('pages/', 'trivia.html')
    elif url.endswith("trivia.css"):
        return send_from_directory('pages/', 'trivia.css')
    else:
        abort(404)

@app.errorhandler(403)
def forbidden(e):
    return send_from_directory('pages/', '403.html'), 403

@app.errorhandler(404)
def notfound(e):
    return send_from_directory('pages/', '404.html'), 404

if __name__ == "__main__":
    app.run(debug=config["SERVER"]["DEBUG"], host='0.0.0.0', port = config["SERVER"]["PORT"])
