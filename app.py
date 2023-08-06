import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient

def create_app():
    app = Flask(__name__)
    client = MongoClient(
        "DB URI")
    db = client.microblog


    @app.route("/", methods=["GET", "POST"])
    def home():
        print("database entries -> ", [e for e in db.entries.find({})])
        if request.method == "POST":
            entry_content = request.form.get("content")
            formattedDateTime = datetime.datetime.today().strftime("%Y-%m-%d")

            db.entries.insert(
                {"content": entry_content, "date": formattedDateTime})
        entries_with_dates = [
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
            )
            for entry in db.entries.find({})
        ]

        return render_template("home.html", entries=entries_with_dates)

    return app
