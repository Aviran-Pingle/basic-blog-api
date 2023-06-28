def validate_post_data(post: dict) -> str:
    """
    Validates the data of a post by checking if the required fields
    are present.

    Param:
        post (dict): A dictionary representing a post.
    Returns:
        str: A string listing the missing fields separated by 'and'.
    """
    fields = ['title', 'content']
    missing_fields = []
    for field in fields:
        if not post.get(field) or field not in post:
            missing_fields.append(field)
    return ' and '.join(missing_fields)


def find_post_by_id(posts: list[dict], post_id: int) -> dict | None:
    """
    Finds a post by its ID in a list of posts.

    Params:
        posts (list[dict]): A list of dictionaries representing posts.
        post_id (int): The ID of the post to be found.
    Returns:
        dict or None: The post dictionary if found, or None if not found.
    """
    for post in posts:
        if post['id'] == post_id:
            return post


def get_sorted_posts(sorting_params: dict, posts: list[dict]) -> list[dict]:
    """
    Sorts a list of posts based on the provided sorting parameters.

    Params:
        sorting_params (dict): A dictionary containing the sorting parameters.
        posts (list[dict]): A list of dictionaries representing posts.
    Returns:
        list[dict]: A sorted list of posts.
    """
    rev = sorting_params['direction'] == 'desc'
    return sorted(posts, key=lambda post: post[sorting_params['sort']],
                  reverse=rev)


def check_sorting_params(sorting_params: dict) -> bool:
    """
    Checks if the provided sorting parameters' values are valid.

    Param:
        sorting_params (dict): A dictionary containing the sorting parameters.
    Returns:
        bool: True if the sorting parameters are valid, False otherwise.
    """
    return (sorting_params['sort'] in ['title', 'content']
            and sorting_params['direction'] in ['asc', 'desc'])
