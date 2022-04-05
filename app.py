from pydoc import render_doc
from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User, Post, Tag, PostTag
from sqlalchemy import desc

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secretsecret'

connect_db(app)
db.create_all()

#USER routes

@app.route('/')
def show_home():
    """show home page"""
    posts = Post.query.order_by(desc(Post.created_at)).limit(5).all()
    return render_template('home.html', posts=posts)

@app.route('/users')
def show_users():
    """Show list of all users"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def new_user_form():
    """Form to add users"""
    return render_template('new_user_form.html')

@app.route('/users/new', methods=["POST"])
def add_user():
    """Adds new user to DB and redirects to new users detail page"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    img_url = request.form["img_url"]
    new_user = User(first_name=first_name, last_name=last_name, img_url=img_url)
    db.session.add(new_user)
    db.session.commit()
    flash('User Successfully Added', 'success')
    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_details(user_id):
    """Show user's detail page"""
    user = User.query.get_or_404(user_id)
    posts = db.session.query(Post.title, Post.content, Post.id).filter(Post.user_id == user_id).all()
    return render_template('user_details.html', user=user, posts=posts)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Show edit user details form"""
    user = User.query.get_or_404(user_id)
    return render_template('edit_user_form.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def handle_edit_user(user_id):
    """Update data base with new values"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.img_url = request.form["img_url"]
    db.session.add(user)
    db.session.commit()
    flash('User Successfully Updated', 'success')
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def handle_delete_user(user_id):
    """Delete a User using session query so delete cascade works"""
    user = db.session.query(User).filter_by(id = user_id).first()
    db.session.delete(user)
    db.session.commit()
    flash('User Successfully Deleted', 'success')
    return redirect('/users')

#POST Routes

@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    """Show new post form"""
    tags = Tag.query.all()
    return render_template('new_post_form.html', user_id=user_id, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def handle_new_post(user_id):
    """Update posts table in DB"""
    title = request.form['title']
    content = request.form['content']
    tag_ids = [int(n) for n in request.form.getlist('tag_input')]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    new_post = Post(title=title, content=content, user_id=user_id, tag=tags)
    # tag_ids = request.form.getlist('tag_input')
    # for tag_id in tag_ids:
    #     db_tag = Tag.query.get(tag_id)
    #     db_tag.categories.append(PostTag(post_id=new_post.id, tag_id=tag_id))
    db.session.add(new_post)
    db.session.commit()
    flash('Post Successfully Created', 'success')
    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """show post from user"""
    post = Post.query.get_or_404(post_id)
    return render_template('post_details.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """show post edit form"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all() 
    current_tag_ids = [tag.id for tag in post.tag]
    return render_template('edit_post_form.html', post=post, tags=tags, current_tag_ids=current_tag_ids)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def handle_post_edit(post_id):
    """show post edit form"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    tag_ids = [int(n) for n in request.form.getlist('tag_input')]
    post.tag = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    db.session.add(post)
    db.session.commit()
    flash('Post Successfully Updated', 'success')
    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def handle_delete_post(post_id):
    """Delete a post using session query so delete cascade works"""
    post = db.session.query(Post).filter(Post.id == post_id).first()
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()
    flash('Post Successfully Deleted', 'success')
    return redirect(f'/users/{user_id}')

#TAG ROUTES

@app.route('/tags')
def show_tags():
    """show list of tags"""
    tags = Tag.query.order_by(Tag.name).all()
    return render_template('tags_index.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag_details(tag_id):
    """show tag details page"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag_details.html', tag=tag)

@app.route('/tags/new')
def new_tag_form():
    """show new tag form"""
    return render_template('new_tag_form.html')

@app.route('/tags/new', methods=['POST'])
def handle_new_tag():
    """handle new tag submission"""
    name = request.form['name']
    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()
    flash ('Tag Successfully Created', 'success')
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    """show tag edit form"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('edit_tag_form.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def handle_edit_tag(tag_id):
    """update db with new tag data"""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    db.session.add(tag)
    db.session.commit()
    flash('Tag Successfully Updated', 'success')
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def handle_delete_tag(tag_id):
    """Remove tag fom DB"""
    tag = db.session.query(Tag).filter(Tag.id == tag_id).first()
    db.session.delete(tag)
    db.session.commit()
    flash('Tag Successfully Deleted', 'success')
    return redirect('/tags')