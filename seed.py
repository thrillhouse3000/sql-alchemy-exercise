from models import User, db
from app import app

db.drop_all()
db.create_all()

User.query.delete()

wilford = User(first_name='Wilford', last_name='Brimley', img_url='https://www.emmys.com/sites/default/files/bios/wilford-brimley-450x600.jpg')

richard =  User(first_name='Richard', last_name='Simmons', img_url='https://assets.vogue.com/photos/58b732ae61606a75f4401afa/master/pass/00-square-richard-simmons-news.jpg')

bob = User(first_name='Bob', last_name='Ross', img_url='https://www.bobross.com/content/bob_ross_img.png')

db.session.add(wilford)
db.session.add(richard)
db.session.add(bob)
db.session.commit()