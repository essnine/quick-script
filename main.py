from os import getenv
import sqlite3

import uvicorn
from quart import Quart

app = Quart(__name__, static_folder="static/")
BASE_HTML = open("static/base.html", "r").read()

APP_PORT = int(getenv("APP_PORT", 80))
APP_HOST = getenv("APP_HOST", "0.0.0.0")


class SimpleView:
    methods = ['GET']

    async def dispatch_request(id):
        return f"ID is {id}"


def load_posts():
    paths = {}
    try:
        db_conn = sqlite3.connect("site.sqlite.db")
        db_conn.row_factory = sqlite3.Row
        posts = [
            dict(row) for row in db_conn.execute("select * from POSTS").fetchall()
        ]
        post_list = [f"<li><a href={post['path']}>{post['title']}</a></li>" for post in posts]
        post_text = "\n".join(post_list)
        post_content = f"<ul>{post_text}</ul>"
        for post in posts:
                paths[post["path"]] = BASE_HTML.format(
                post_list=post_content,
            body_content=eval(post["md"]).decode("utf-8")
            )
    except Exception as exc:
        app.logger.exception(f"Exception raised when loading posts from posts db {str(exc)}", stack_info=True)
        exit()
        app.add_url_rule(post['path'], view_func=SimpleView.as_view('simple'))
    return paths


PATHS = load_posts()


@app.route("/posts")
def get_all_posts_list():
    ...


@app.route("/")
def load_root():
    return PATHS["/"], 200


app.add_url_rule(rule, options)


@app.route("/<string:route>")
def load_page(route):
    app.logger.warning(f"Trying to fetch route: {route}")
    if route.endswith(".html"):
        route = route[:-5]
    if f"/{route}" in PATHS:
        return PATHS[f"/{route}"], 200
    else:
        print("Could not find route!")
        return "Not found!", 404


def main():
    app.logger.info(PATHS.keys())
    uvicorn.run(app=app, host=APP_HOST, port=APP_PORT)


if __name__ == "__main__":
    main()
