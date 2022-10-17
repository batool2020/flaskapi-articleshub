from flask import render_template, request, Blueprint
from flaskarticles.Models.models import Post
from flaskarticles import  cache
from flaskarticles.utils import docache

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
@cache.cached(timeout=70)
def home():  # put application's code here
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=5) # pagination with default page =1, 5 number of pages per page, sort descinding so the last arrticles show up first
    return render_template('home.html', posts=posts)


@main.route('/about')
@cache.cached(timeout=70)
def about():  # put application's code here
    return render_template('about.html', title='About')



