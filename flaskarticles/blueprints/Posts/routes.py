from flask import (render_template, url_for, flash, redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskarticles import db, cache
from flaskarticles.Models.models import Post
from flaskarticles.blueprints.Posts.forms import PostForm, SearchForm, DateForm
from flaskarticles.utils import docache
from sqlalchemy import or_, and_

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
def base2():
    form2 = DateForm()
    return dict(form=form2)




# FIX THE FILTER TECH AND ADD OTHER FILTERS
## THEN GO TO DOCUMENTATION AND SUBMITTTTT

@posts.route("/filter-tech")
@docache(minutes=5, content_type='post.html')
def filter_tech():

    page = request.args.get('page', 1, type=int)
    postslist = Post.query.filter(or_(Post.title.contains('Python'), Post.title.contains('Program'), Post.title.contains('Flask'))) \
        .paginate(page=page, per_page=6)
    flash('Filter Result: Technology related Topics', 'success')
    return render_template('techFilter.html', posts=postslist)


@posts.route("/filter-tips")
@docache(minutes=5, content_type='post.html')
def filter_tips():
        page = request.args.get('page', 1, type=int)
        postslist = Post.query.filter(Post.title.contains(" % Tips % ")) \
            .paginate(page=page, per_page=6)
        flash('Filter Result: Tips', 'success')
        return render_template('tipsFilter.html', posts=postslist)


@posts.route("/filter-youtube")
@docache(minutes=5, content_type='post.html')
def filter_youtube():
        page = request.args.get('page', 1, type=int)
        postslist = Post.query.filter(Post.title.contains(" % Youtube % ")) \
            .paginate(page=page, per_page=6)
        flash('Filter Result: Social Medial- Youtube', 'success')
        return render_template('youtubeFilter.html', posts=postslist)

@posts.route("/filter-before", methods = ['GET','POST'])
@docache(minutes=5, content_type='post.html')
def filter_before():
    global start
    global end
    if request.method == 'POST':
        form2 = DateForm()
        start = form2.startDate.data
        end = form2.endDate.data
        if form2.validate_on_submit():
            page = request.args.get('page', 1, type=int)
            start = request.args.get('start', form2.startDate.data)
            end = request.args.get('end', form2.endDate.data)
            postslist = Post.query.filter(and_(Post.date_posted < end, Post.date_posted >= start)) \
           .paginate(page=page, per_page=4)
            flash('Search Result', 'success')
            return render_template('beforeFilter.html', posts=postslist, form=form2)
        flash('No Filter Result', 'danger')
        return redirect(url_for('main.home'))
    else:
        form3 = DateForm()
        page = request.args.get('page', 1, type=int)
        form3.startDate.data = start
        form3.endDate.data = end
        postslist = Post.query.filter(and_(Post.date_posted < end, Post.date_posted >= start)) \
            .paginate(page=page, per_page=4)
        flash('Search Result', 'success')
        return render_template('beforeFilter.html', posts=postslist, form=form3)


