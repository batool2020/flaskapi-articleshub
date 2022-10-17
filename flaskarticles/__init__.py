from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flaskarticles.config import Config
from flaskarticles.blueprints.Posts.forms import SearchForm
from flask_migrate import Migrate
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
migrate = Migrate()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    #pass the application to all of the extentions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from flaskarticles.blueprints.Users.routes import users
    from flaskarticles.blueprints.Posts.routes import posts
    from flaskarticles.blueprints.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)

    @app.context_processor
    def base():
        form = SearchForm()
        return dict(form=form)

    return app


# PAss Form to NavBar

