

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

@app.route("/<name>")
def hello(name):
    if '..' in name or '~' in name:
        abort(403)
    elif os.path.isfile(name):
        return send_from_directory('pages/', name)
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
