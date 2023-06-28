from flask import Blueprint, request, jsonify

import auxiliary_functions
import backend_app as app

bp = Blueprint('routes', __name__)


@bp.route('/api/posts', methods=['GET'])
def get_posts():
    """
    Get all posts or sorted posts based on provided parameters.

    Params:
        sort (str): The field to sort the posts by.
        direction (str): The sorting direction ('asc' or 'desc').
    Returns:
        List of posts.
    """
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
    """
    Add a new post.
    Get the JSON object representing the new post from the request body.
    Returns:
        The newly added post.
    """
    new_post = request.get_json()

    if missing_fields := auxiliary_functions.validate_post_data(new_post):
        return jsonify({'error': f'Missing {missing_fields}'}), 400

    new_id = max(post['id'] for post in app.POSTS) + 1 if app.POSTS else 1
    new_post['id'] = new_id
    app.POSTS.append(new_post)

    return jsonify(new_post), 201


@bp.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """
    Delete a post by ID.

    Param:
        post_id (int): The ID of the post to be deleted.
    Returns:
        A success message if the post is deleted.
    """
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
    """
    Update a post by ID.
    Get the JSON object representing the updated post data from the
    request body.

    Param:
        post_id (int): The ID of the post to be updated.
    Returns:
        The updated post.
    """
    post_to_be_updated = auxiliary_functions.find_post_by_id(app.POSTS,
                                                             post_id)
    if not post_to_be_updated:
        return jsonify({'error': f'Post with id {post_id} not found'}), 404

    new_post_data = request.get_json()
    post_to_be_updated.update(new_post_data)
    return jsonify(post_to_be_updated)


@bp.route('/api/posts/search')
def search_posts():
    """
    Search posts based on provided search parameters.

    Params:
        title (str, optional): The title keyword to search for.
        content (str, optional): The content keyword to search for.
    Returns:
        List of posts that match the search criteria.
    """
    params = request.args
    matched_posts = set()
    for field in ['title', 'content']:
        if field in params:
            matched_by_field = {tuple(post.items()) for post in app.POSTS
                                if params[field] in post[field]}
            matched_posts = matched_posts.union(matched_by_field)

    return jsonify([dict(post) for post in matched_posts])
