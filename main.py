import sqlite3

import uvicorn
from quart import Quart

app = Quart(__name__, static_folder="static/")
BASE_HTML = open("static/base.html", "r").read()


def load_posts():
    paths = {}
    db_conn = sqlite3.connect("site.sqlite.db")
    db_conn.row_factory = sqlite3.Row
    posts = [dict(row) for row in db_conn.execute("select * from POSTS").fetchall()]
    for post in posts:
        paths[post["path"]] = BASE_HTML.format(
            body_content=eval(post["md"]).decode("utf-8")
        )
    return paths


PATHS = load_posts()


@app.route("/")
def home():
    return PATHS["home.html"], 200


@app.route("/<route>")
def load_page(route):
    if route in PATHS:
        return PATHS[route], 200
    else:
        return "Not found!", 404


def main():
    load_posts()
    uvicorn.run(app=app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
