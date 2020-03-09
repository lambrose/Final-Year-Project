from loop import create_app
from flask_talisman import Talisman

app = create_app()

if __name__ == '__main__':
    # redirect to https
    Talisman(app)
    app.run(debug=True)
