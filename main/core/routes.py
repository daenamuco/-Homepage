from flask import render_template, request, Blueprint
from main import pnhl
from main.models import Post
from flask_login import login_required


core = Blueprint('core', __name__)



@core.route("/")
@core.route("/home")
def home():
        return render_template("index.html", news=pnhl)



@core.route("/community")
@login_required
def community():
        page = request.args.get('page', 1, type=int)
        # page argument를 가져오는데 default를 1로 정하고 int만 받기로해서 int가 아니면 에러 
        posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
        # paginate로 페이지를 생성, per_page는 각 페이지마다 있을 page를 지정, page는 위의 argument
        # order_by로 표시할 순서 지정, desc로 내림차순(최신이 먼저)
        return render_template('community.html', posts=posts)