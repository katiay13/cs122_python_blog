# Flask is Web framework 
# Load HTML files from templates/
from flask import Flask, render_template, session, request, redirect, url_for

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


# runs when 'fashion reviews' tab is visited
@app.route("/fashion-reviews")
def fashion_reviews():
    return render_template("fashion_reviews.html")

# decides if player has everything the hotspot requires
def has_all(flags, requires):
    if requires is None:        # no requirement
        return True             # always allowed
    if isinstance(requires, str):  # if req is str, wrap in list 
        requires = [requires]
    for flag in requires:       # for every required flag
        if flag not in flags:   # check if a requirement is missing
            return False
    return True

# runs when someone visits /mysterious-castle
# route accepts form submissions
@app.route("/mysterious-castle", methods=["GET", "POST"])
def play():
    scene_id = session.get("scene", "castle_exterior")  # grabs scene id, default: castle_exterior
    path = os.path.join(app.root_path, "interactive", "scenes.json")    # full path to json file
    with open(path, encoding="utf-8") as f:
        scenes = json.load(f)   # store json text as python dict
    scene = scenes[scene_id]    # grabs scene's data (name, dialogue, hotspots)

    if request.method == "POST":
        clicked_id = request.form.get("hotspot")
        flags = session.get("flags", [])
        message = None

        for hotspot in scene["hotspots"]:
            if hotspot["id"] == clicked_id:
                requires = hotspot.get("requires")
                gives = hotspot.get("gives")

                if gives and gives in flags:
                    message = hotspot.get("done_text")
                elif not has_all(flags, requires):
                    message = hotspot.get("not_yet_text")
                else:
                    if gives:
                        flags.append(gives)
                    if hotspot["type"] == "exit":
                        session["scene"] = hotspot["target"]
                    message = hotspot.get("text")
        
        if message:
            session["look_text"] = message
        session["flags"] = flags
        return redirect(url_for("play"))

    dialogue = session.pop("look_text", scene["dialogue"])
    return render_template("castle.html", scene=scene, dialogue=dialogue)

@app.route("/mysterious-castle/restart")
def restart():
    session.pop("scene", None)
    session.pop("look_text", None)
    session.pop("flags", None)
    return redirect(url_for("play"))

# NEEDS to stay at BOTTOM of file
# Runs when file is started with "python app.py"
if __name__ == "__main__":
    with app.app_context(): # Need app context for database commands
        db.create_all() # Creates pythonistas_blog.db and any other tables
    app.run(debug=True) # Will auto reload when changes are saved
