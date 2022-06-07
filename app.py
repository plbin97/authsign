from flask import Flask, redirect
from src.app import auth_sign

app = Flask(__name__, static_folder=None)
app.register_blueprint(auth_sign)


@app.route('/')
def index():
    return redirect('/authsign')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088)
