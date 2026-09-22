import datetime
from database.models import Comment

def create_comment(photo_name, author, content):
    comment = Comment.create(photo_name=photo_name, author=author, content=content, created_at=datetime.datetime.now())
    return comment