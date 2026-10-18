import peewee
import datetime

db = peewee.SqliteDatabase('content/data.db')

class Comment(peewee.Model):
    id = peewee.AutoField()
    photo_name = peewee.CharField(max_length=255)
    author = peewee.CharField(max_length=100)
    content = peewee.TextField()
    created_at = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

class Blog_Comment(peewee.Model):
    id = peewee.AutoField()
    blog_name = peewee.CharField(max_length=255)
    author = peewee.CharField(max_length=100)
    content = peewee.TextField()
    refrence = peewee.ForeignKeyField(
        'self',
        null=True,
        backref='replies',
        column_name='reference_id',
    )
    created_at = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

class Views(peewee.Model):
    id = peewee.AutoField()
    blog_name = peewee.CharField(max_length=255)
    remote_ip = peewee.CharField()
    time_spend = peewee.IntegerField()

    class Meta:
        database = db

def init_db():
    db.connect()
    db.create_tables([Comment, Blog_Comment, Views], safe=True)
    db.close()