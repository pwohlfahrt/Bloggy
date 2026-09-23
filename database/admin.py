from database.models import Comment

def delete_comment(id: int):
    Comment.delete().where(Comment.id == id).execute()
    return {'status': "ok"}