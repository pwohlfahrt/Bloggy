import peewee
from database.models import Views, Comment, Blog_Comment

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
    comments = [
        {
            "author": comment.author,
            "content": comment.content,
            "id": comment.id,
            "blog_comment": False,
        }
        for comment in (Comment
                        .select(Comment.author, Comment.content, Comment.id)
                        .order_by(Comment.created_at.desc())
                        .limit(num))
    ]
    comments += [
        {
            "author": comment.author,
            "content": comment.content,
            "id": comment.id,
            "blog_comment": True,
        }
        for comment in (Blog_Comment
                        .select(Blog_Comment.author, Blog_Comment.content, Blog_Comment.id)
                        .order_by(Blog_Comment.created_at.desc())
                        .limit(num))
    ]
    return sorted(comments, key=lambda comment: comment["id"], reverse=True)[:num]

def unique_views():
    res = (Views
           .select(Views.blog_name, peewee.fn.COUNT(peewee.fn.DISTINCT(Views.remote_ip)).alias("viewers"))
           .group_by(Views.blog_name))
    return [
        {
            "blog": blog.blog_name,
            "viewers": getattr(blog, "viewers", 0)
        }
        for blog in res
    ]