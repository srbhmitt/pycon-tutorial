from flask import Flask

# Initialize the Flask application
app = Flask(__name__)

from app import views

if __name__ == '__main__':
    app.run(debug=True)
