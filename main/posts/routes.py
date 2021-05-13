from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from main import db
from main.models import Post
from main.posts.forms import PostForm

posts = Blueprint('posts', __name__)




@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
# 로그인해야 접속할 수 있게 만들어줌
def new_post():
        form = PostForm()
        if form.validate_on_submit():
                post = Post(title=form.title.data, content=form.content.data, author=current_user)
                # 폼 데이터를 하나로 정리
                db.session.add(post)
                db.session.commit()
                # db에 post 내용 추가함
                flash('Your post has been created!', 'success')
                return redirect(url_for('core.community'))
        return render_template("create_post.html", form=form, legend='New Post')



@posts.route("/post/<int:post_id>")
# int: 는 post id가 int임을 알려줌
def post(post_id):
        post = Post.query.get_or_404(post_id)
        # get_or_404 -> get을 시도하고 값이 존재하지 않으면 404출력
        return render_template('post.html', title=post.title, post=post)



@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
        post = Post.query.get_or_404(post_id)
        if post.author != current_user:
                abort(403)
                # abort는 스크립트를 중지함, 403은 forbidden된 문서를 표시할때 오류
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
        return render_template('create_post.html', form=form, legend='Update Post')



@posts.route("/post/<int:post_id>/delete", methods=['POST'])
# post 방식의 데이터 전송만 받을거라는 것임 -> form의 전송방식이 POST여서 그럼 
@login_required
def delete_post(post_id):
        post = Post.query.get_or_404(post_id)
        if post.author != current_user:
                abort(403)
                # abort는 스크립트를 중지함, 403은 forbidden된 문서를 표시할때 오류
        db.session.delete(post)
        db.session.commit()
        flash('Your post has been deleted!', 'success')
        return redirect(url_for('core.community'))