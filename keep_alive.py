from flask import Flask
from threading import Thread



app = Flask('')


@app.route('/')
def home():
    return "Active!"


@app.route('/items.json')
def items():
    with open('data/items.json')as f:
        return f.read()

@app.route('/locations.json')
def locations():
    with open('data/locations.json')as f:
        return f.read()

@app.route('/skills.json')
def skills():
    with open('data/skills.json')as f:
        return f.read()


# @app.errorhandler(404)
# def page_not_found(e):
#     return er404

def run():
    app.run(host='0.0.0.0', port=6699)


def keep_alive():
    t = Thread(target=run)
    t.start()
