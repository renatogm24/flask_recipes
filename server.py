from flask_app.controllers import users
from flask_app.controllers import recipes
from flask_app import app

if __name__ == "__main__":
    import logging
    logging.basicConfig(filename='error.log',level=logging.DEBUG)
    app.run(debug=True)