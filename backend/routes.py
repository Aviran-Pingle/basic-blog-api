from flask import Blueprint, request, jsonify

import auxiliary_functions
import backend_app as app

bp = Blueprint('routes', __name__)


@bp.route('/api/posts', methods=['GET'])
def get_posts():
    params = request.args
    if 'sort' in params and 'direction' in params:
        is_valid_vals = auxiliary_functions.check_sorting_params(params)
        if not is_valid_vals:
            return jsonify({'error': 'wrong sorting param value'}), 400
        return jsonify(auxiliary_functions.get_sorted_posts(params, app.POSTS))

    if 'sort' in params or 'direction' in params:
        return jsonify({'error': 'missing one sorting param'}), 400

    return jsonify(app.POSTS)


@bp.route('/api/posts', methods=['POST'])
def add_post():
    new_post = request.get_json()

    if missing_fields := auxiliary_functions.validate_post_data(new_post):
        return jsonify({'error': f'Missing {missing_fields}'}), 400

    new_id = max(post['id'] for post in app.POSTS) + 1 if app.POSTS else 1
    new_post['id'] = new_id
    app.POSTS.append(new_post)

    return jsonify(new_post), 201


@bp.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post_to_be_deleted = auxiliary_functions.find_post_by_id(app.POSTS,
                                                             post_id)
    if not post_to_be_deleted:
        return jsonify({'error': f'Post with id {post_id} not found'}), 404

    del app.POSTS[app.POSTS.index(post_to_be_deleted)]
    return jsonify({
        'message': f'Post with id {post_id} has been deleted successfully.'
    })


@bp.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post_to_be_updated = auxiliary_functions.find_post_by_id(app.POSTS,
                                                             post_id)
    if not post_to_be_updated:
        return jsonify({'error': f'Post with id {post_id} not found'}), 404

    new_post_data = request.get_json()
    post_to_be_updated.update(new_post_data)
    return jsonify(post_to_be_updated)


@bp.route('/api/posts/search')
def search_posts():
    params = request.args
    matched_posts = set()
    for field in ['title', 'content']:
        if field in params:
            matched_by_field = {tuple(post.items()) for post in app.POSTS
                                if params[field] in post[field]}
            matched_posts = matched_posts.union(matched_by_field)

    return jsonify([dict(post) for post in matched_posts])
