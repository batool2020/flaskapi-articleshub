from flask import (render_template, url_for, flash, redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskarticles import db
from flaskarticles.Models.models import Post
from flaskarticles.blueprints.Posts.forms import PostForm, SearchForm, SimpleForm
from flaskarticles.utils import docache
from sqlalchemy import or_


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
@docache(minutes=5, content_type='post.html')
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
        return render_template('post.html', title=post.title, post=post)

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


@posts.route("/search", methods=['POST'])
def search():
    form1 = SearchForm()
    if form1.validate_on_submit():
        page = request.args.get('page', 1, type=int)
        postslist = Post.query.filter(Post.title.contains(form1.content.data))\
            .paginate(page=page)
        flash('Search Result', 'success')
        return render_template('searchposts.html', posts=postslist, form=form1)
    flash('No Search Result', 'danger')
    return redirect(url_for('main.home'))


# FIX THE FILTER TECH AND ADD OTHER FILTERS
## THEN GO TO DOCUMENTATION AND SUBMITTTTT

@posts.route("/filter-tech")
def filter_tech():

    page = request.args.get('page', 1, type=int)
    postslist = Post.query.filter(or_(Post.title.contains('Python'), Post.title.contains('Program'), Post.title.contains('Flask'))) \
        .paginate(page=page, per_page=6)
    flash('Filter Result: Technology related Topics', 'success')
    return render_template('techFilter.html', posts=postslist)


@posts.route("/filter-tips")
def filter_tips():
        page = request.args.get('page', 1, type=int)
        postslist = Post.query.filter(Post.title.contains(" % Tips % ")) \
            .paginate(page=page, per_page=6)
        flash('Filter Result: Tips', 'success')
        return render_template('tipsFilter.html', posts=postslist)


@posts.route("/filter-youtube")
def filter_youtube():
        page = request.args.get('page', 1, type=int)
        postslist = Post.query.filter(Post.title.contains(" % Youtube % ")) \
            .paginate(page=page, per_page=6)
        flash('Filter Result: Social Medial- Youtube', 'success')
        return render_template('youtubeFilter.html', posts=postslist)

@posts.route("/filter-before")
def filter_before():
        page = request.args.get('page', 1, type=int)
        postslist = Post.query.filter(Post.date_posted < '2022-10-14') \
            .paginate(page=page, per_page=6)
        flash('Filter Result', 'success')
        return render_template('beforeFilter.html', posts=postslist)

@posts.route("/filter-after")
def filter_after():
        page = request.args.get('page', 1, type=int)
        postslist = Post.query.filter( '2022-10-14' <= Post.date_posted ) \
            .paginate(page=page, per_page=6)
        flash('Filter Result', 'success')
        return render_template('afterFilter.html', posts=postslist)

