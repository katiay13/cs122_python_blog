# Flask is Web framework 
# Load HTML files from templates/
from flask import Flask, render_template, session

import json
import os

# Connect Flask to database
from flask_sqlalchemy import SQLAlchemy

# Create Flask app
app = Flask(__name__)

# for interactive game
app.config["SECRET_KEY"] = "dev-key-change-later"

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

# runs when developers tab is visited
@app.route("/developers")
def developers():
    return render_template("developers.html")

# runs when 'music reviews' tab is visited
@app.route("/music-reviews")
def music_reviews():
    return render_template("music_reviews.html")

# runs when someone visits /mysterious-castle
@app.route("/mysterious-castle")
def play():
    scene_id = session.get("scene", "castle_exterior")  # grabs scene id, default: castle_exterior
    path = os.path.join(app.root_path, "interactive", "scenes.json")    # full path to json file
    with open(path, encoding="utf-8") as f:
        scenes = json.load(f)   # store json text as python dict
    scene = scenes[scene_id]    # grabs scene's data (name, dialogue, hotspots)
    return render_template("castle.html", scene=scene)

# NEEDS to stay at BOTTOM of file
# Runs when file is started with "python app.py"
if __name__ == "__main__":
    with app.app_context(): # Need app context for database commands
        db.create_all() # Creates pythonistas_blog.db and any other tables
    app.run(debug=True) # Will auto reload when changes are saved
