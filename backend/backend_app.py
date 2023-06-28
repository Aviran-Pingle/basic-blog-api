from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def validate_post_data(post: dict):
    fields = ['title', 'content']
    missing_fields = []
    for field in fields:
        if not post.get(field) or field not in post:
            missing_fields.append(field)
    return ' and '.join(missing_fields)


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    new_post = request.get_json()

    if missing_fields := validate_post_data(new_post):
        return jsonify({'error': f'Missing {missing_fields}'}), 400

    new_id = max(post['id'] for post in POSTS) + 1 if POSTS else 1
    new_post['id'] = new_id
    POSTS.append(new_post)

    return jsonify(new_post), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
