from flask import Flask, jsonify, request
from flask_cors import CORS

import auxiliary_functions

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    params = request.args
    if 'sort' in params and 'direction' in params:
        is_valid_vals = auxiliary_functions.check_sorting_params(params)
        if not is_valid_vals:
            return jsonify({'error': 'wrong sorting param value'}), 400
        return jsonify(auxiliary_functions.get_sorted_posts(params, POSTS))

    if 'sort' in params or 'direction' in params:
        return jsonify({'error': 'missing one sorting param'}), 400

    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    new_post = request.get_json()

    if missing_fields := auxiliary_functions.validate_post_data(new_post):
        return jsonify({'error': f'Missing {missing_fields}'}), 400

    new_id = max(post['id'] for post in POSTS) + 1 if POSTS else 1
    new_post['id'] = new_id
    POSTS.append(new_post)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post_to_be_deleted = auxiliary_functions.find_post_by_id(POSTS, post_id)
    if not post_to_be_deleted:
        return jsonify({'error': f'Post with id {post_id} not found'}), 404

    del POSTS[POSTS.index(post_to_be_deleted)]
    return jsonify({
        'message': f'Post with id {post_id} has been deleted successfully.'
    })


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post_to_be_updated = auxiliary_functions.find_post_by_id(POSTS, post_id)
    if not post_to_be_updated:
        return jsonify({'error': f'Post with id {post_id} not found'}), 404

    new_post_data = request.get_json()
    post_to_be_updated.update(new_post_data)
    return jsonify(post_to_be_updated)


@app.route('/api/posts/search')
def search_posts():
    params = request.args
    matched_posts = set()
    for field in ['title', 'content']:
        if field in params:
            matched_by_field = {tuple(post.items()) for post in POSTS
                                if params[field] in post[field]}
            matched_posts = matched_posts.union(matched_by_field)

    return jsonify([dict(post) for post in matched_posts])


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
