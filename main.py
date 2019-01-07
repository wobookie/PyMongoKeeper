import secrets
from flask import Flask
from flask_login import LoginManager

# Blueprints
from app.errors import handlers as errors
from app.auth import login as login
from app.dashboard import dashboard as dashboard

# Model
from app.models import user

# Init App
app = Flask(__name__)

# Secret Key
app.config['SECRET_KEY'] = secrets.token_urlsafe(20)
app.config['PAGE_SIZE'] = 10

# login manager needs be set before blueprint registration
login_manager = LoginManager()
login_manager.init_app(app)

app.register_blueprint(errors.bp)
app.register_blueprint(login.bp)
app.register_blueprint(dashboard.bp)

@login_manager.user_loader
def load_user(user_id):
    return user.User(user_id)


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
