from flask import redirect
from appFactory import createApp

app = createApp()
from src.authsign.databaseModels import User
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = None

@app.route('/')
def index():
    return redirect('/authsign')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088)
