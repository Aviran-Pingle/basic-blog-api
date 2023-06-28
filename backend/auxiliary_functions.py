def validate_post_data(post: dict):
    fields = ['title', 'content']
    missing_fields = []
    for field in fields:
        if not post.get(field) or field not in post:
            missing_fields.append(field)
    return ' and '.join(missing_fields)


def find_post_by_id(posts: list[dict], post_id: int):
    for post in posts:
        if post['id'] == post_id:
            return post


def get_sorted_posts(sorting_params, posts):
    rev = sorting_params['direction'] == 'desc'
    return sorted(posts, key=lambda post: post[sorting_params['sort']],
                  reverse=rev)


def check_sorting_params(sorting_params):
    return (sorting_params['sort'] in ['title', 'content']
            and sorting_params['direction'] in ['asc', 'desc'])
