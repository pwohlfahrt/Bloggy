import datetime
from database.models import Blog_Comment


def create_blog_comment(blog, author, content, reference=None):
    normalized_reference = None
    if reference not in (None, ''):
        try:
            normalized_reference = int(reference)
        except (TypeError, ValueError):
            normalized_reference = None

    comment = Blog_Comment.create(
        blog_name=blog,
        author=author,
        content=content,
        refrence=normalized_reference,
        created_at=datetime.datetime.now(),
    )
    return comment


def get_blog_comments(blog: str, offset: int):
    comments = Blog_Comment.select().where(Blog_Comment.blog_name == blog).order_by(Blog_Comment.created_at.desc()).offset(offset).limit(10)
    result = []
    for comment in comments:
        reference_id = getattr(comment, 'reference_id', None)
        ref_value = None
        if reference_id not in (None, '', 0):
            try:
                ref_value = comment.refrence.id
            except Blog_Comment.DoesNotExist:
                ref_value = None

        result.append({
            'id': comment.id,
            'author': comment.author,
            'content': comment.content,
            'created_at': comment.created_at,
            'reference': ref_value,
        })
    return result