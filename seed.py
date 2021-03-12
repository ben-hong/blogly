from models import db, connect_db, BlogUser, Post, Tag, PostTag
from app import app

# Create all tables
db.drop_all()
db.create_all()


ben = BlogUser(first_name='Ben', last_name='Hong', image_url=None)
john = BlogUser(first_name='John', last_name='Shrader', image_url=None)
bob = BlogUser(first_name='Bob', last_name='Builder', image_url=None)

db.session.add(ben)
db.session.add(john)
db.session.add(bob)

db.session.commit()
