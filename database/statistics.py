import peewee
from database.models import Views, Comment

def add_viewing_blog(blog_name: str, ip: str, time_spend: int):
    viewer = Views.get_or_none((Views.blog_name == blog_name) & (Views.remote_ip == ip))
    if viewer != None:
        viewer.time_spend += time_spend
        viewer.save()
    else:
        Views.create(blog_name=blog_name, remote_ip=ip, time_spend=time_spend)

def get_viewing_time_of_blog(blog_name: str):
    return (Views
            .select(peewee.fn.SUM(Views.time_spend).alias('total_time'))
            .where(Views.blog_name == blog_name)
            .scalar() or 0)

def get_latest_comments(num: int) -> list[dict]:
    res = (Comment
                .select(Comment.author, Comment.content, Comment.id)
                .order_by(Comment.created_at.desc())
                .limit(num))
    return [{"author": comment.author, "content": comment.content, "id": comment.id} for comment in res]