from models import User, Post, db
from app import app

db.drop_all()
db.create_all()

User.query.delete()
Post.query.delete()


mrt =  User(first_name='Mr.', last_name='T', img_url='https://cdn.mos.cms.futurecdn.net/mFDumCYxaHBY8FdmyQxn4i-1024-80.jpg.webp')

bob = User(first_name='Bob', last_name='Ross', img_url='https://www.bobross.com/content/bob_ross_img.png')

post1 = Post(title='I pity the fool!', content="That doesn't respect his mother", user_id=1)

post2 = Post(title='Happy little tree', content='There are no mistakes, just happy accidents', user_id=2)

db.session.add_all([mrt, bob, post1, post2])
db.session.commit()