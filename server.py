from flask_app.controllers import user_cont
from flask_app.controllers import expenses_cont
from flask_app.controllers import group_cont

from flask_app import app

if __name__ == "__main__":
    app.run(debug=True)