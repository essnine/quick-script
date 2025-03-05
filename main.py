from os import getenv
import sqlite3

import uvicorn
from quart import Quart

app = Quart(__name__, static_folder="static/")
BASE_HTML = open("static/base.html", "r").read()

APP_PORT = int(getenv("APP_PORT", 80))
APP_HOST = getenv("APP_HOST", "0.0.0.0")


def load_posts():
    paths = {}
    db_conn = sqlite3.connect("site.sqlite.db")
    db_conn.row_factory = sqlite3.Row
    posts = [
        dict(row) for row in db_conn.execute("select * from POSTS").fetchall()
    ]
    for post in posts:
        paths[post["path"]] = BASE_HTML.format(
            body_content=eval(post["md"]).decode("utf-8")
        )
    return paths


PATHS = load_posts()


@app.route("/")
def load_root():
    return PATHS["/"], 200


@app.route("/<route>")
def load_page(route=None):
    if f"/{route}" in PATHS:
        return PATHS[f"/{route}"], 200
    else:
        return "Not found!", 404


def main():
    print(PATHS.keys())
    uvicorn.run(app=app, host=APP_HOST, port=APP_PORT)


if __name__ == "__main__":
    main()
