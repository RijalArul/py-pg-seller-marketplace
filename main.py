from flask import Flask
from routes.offer import offer_routes


app = Flask(__name__)

app.register_blueprint(offer_routes)

if __name__ == '__main__':
    app.run(debug=True, port=8080)

