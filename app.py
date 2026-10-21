# Flask is Web framework 
# Load HTML files from templates/
from flask import Flask, render_template

# Connect Flask to database
from flask_sqlalchemy import SQLAlchemy

# Create Flask app
app = Flask(__name__)

# Database is SQLite file
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pythonistas_blog.db"

# Connect SQLAlchemy to app
db = SQLAlchemy(app)

# Example model for now to test if database works
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)


# Runs when homepage is visited
@app.route("/")
def index():
    return render_template("index.html")

# Runs when file is started with "python app.py"
if __name__ == "__main__":
    with app.app_context(): # Need app context for database commands
        db.create_all() # Creates pythonistas_blog.db and any other tables
    app.run(debug=True) # Will auto reload when changes are saved

# runs when developers tab is visited
@app.route("/developers")
def developers():
    return render_template("developers.html")
