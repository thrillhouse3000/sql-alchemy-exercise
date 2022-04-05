from models import User, Post, Tag, PostTag, db
from app import app

db.drop_all()
db.create_all()

User.query.delete()
Post.query.delete()


mrt =  User(first_name='Mr.', last_name='T', img_url='https://cdn.mos.cms.futurecdn.net/mFDumCYxaHBY8FdmyQxn4i-1024-80.jpg.webp')

bob = User(first_name='Bob', last_name='Ross', img_url='https://www.bobross.com/content/bob_ross_img.png')

post1 = Post(title='I pity the fool!', content="That doesn't respect his mother", user_id=1)

post2 = Post(title='Happy little tree', content='There are no mistakes, just happy accidents', user_id=2)

tag1 = Tag(name='Heart Warming')

tag2 = Tag(name='Good Vibes')

tag3 = Tag(name='Funny')

tag4 = Tag(name='Zen')


db.session.add_all([mrt, bob, post1, post2, tag1, tag2, tag3, tag4])
db.session.commit()

post1 = Post.query.get(1)
post2 = Post.query.get(2)

post1.categories.append(PostTag(post_id=1, tag_id=1))
post1.categories.append(PostTag(post_id=1, tag_id=3))
post2.categories.append(PostTag(post_id=2, tag_id=2))
post2.categories.append(PostTag(post_id=2, tag_id=4))

db.session.add_all([post1, post2])
db.session.commit()