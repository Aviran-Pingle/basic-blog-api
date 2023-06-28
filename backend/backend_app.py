from flask import Flask
from flask_cors import CORS

import routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def main():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(routes.bp)
    app.run(host="0.0.0.0", port=5002, debug=True)


if __name__ == '__main__':
    main()
