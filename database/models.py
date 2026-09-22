import peewee
import datetime

db = peewee.SqliteDatabase('comments.db')

class Comment(peewee.Model):
    id = peewee.AutoField()
    photo_name = peewee.CharField(max_length=255)
    author = peewee.CharField(max_length=100)
    content = peewee.TextField()
    created_at = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

def init_db():
    db.connect()
    db.create_tables([Comment], safe=True)
    db.close()