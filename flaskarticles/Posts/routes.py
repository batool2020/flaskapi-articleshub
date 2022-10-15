from flask import (render_template, url_for, flash, json,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskarticles import db
from flaskarticles.Models.models import Post
from flaskarticles.Posts.forms import PostForm, SearchForm
from flaskarticles.utils import docache

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
@docache(minutes=5, content_type='post.html')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))




# PAss Form to NavBar
@posts.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


@posts.route("/search", methods=["POST"])
def search():
    form1 = SearchForm()
    #posts = Post.query
    if form1.validate_on_submit():
        page = request.args.get('page', 1, type=int)
        postslist = Post.query.filter(Post.title.contains(form1.content.data))\
            .paginate(page=page, per_page=3)
        flash('Search Result', 'success')
        return render_template('searchposts.html', posts=postslist, form=form1)
    flash('No Search Result', 'danger')
    return redirect(url_for('main.home'))



