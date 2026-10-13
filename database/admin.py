from database.models import Comment, Blog_Comment

def delete_comment(id: int, blog_comment: bool = False):
    if blog_comment:
        Blog_Comment.delete().where(Blog_Comment.id == id).execute()
    else:
        Comment.delete().where(Comment.id == id).execute()
    return {'status': "ok"}