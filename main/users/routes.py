from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from main import db, bcrypt
from main.models import User, Post
from main.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, ResetRequestForm, ResetPasswordForm
from main.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)




@users.route("/register", methods=['GET', 'POST'])
def register():
        if current_user.is_authenticated:
                return redirect(url_for('core.home'))
        form = RegistrationForm()
        if form.validate_on_submit():
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                # 입력된 비밀번호를 해시값으로 저장함, decode utf-8은 해시값을 string으로 변환해줌
                user = User(username=form.username.data, email=form.email.data, password=hashed_password)
                # 유저 정보의 db를 생성한다. 비밀번호는 상단 해시값으로!!
                db.session.add(user)
                db.session.commit()
                # db에 정보를 추가 후, commit로 최종결정

                flash(f'Account created for {form.username.data}!', 'success')
                return redirect(url_for('users.login'))
        return render_template("register.html", form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
        if current_user.is_authenticated:
                return redirect(url_for('core.home'))
        form = LoginForm()
        if form.validate_on_submit():
        # validate on submit은 데이터를 전송받았을때 유효한지 검사함
                user = User.query.filter_by(email=form.email.data).first()
                # 유저의 email이 중복되었는지 확인함
                if user and bcrypt.check_password_hash(user.password, form.password.data):
                # 이후 비밀번호가 저장된 해시 변환값과 일치하는지 확인함
                        login_user(user, remember=form.remember.data)
                        # 유저를 로그인 + 다음에도 기억할지 arg도 포함
                        next_page = request.args.get('next')
                        return redirect(next_page) if next_page else redirect(url_for('core.home'))
                else:
                        flash('Login Unsuccessful. Please check email and password', 'danger')
        return render_template("login.html", form=form)


@users.route("/logout")
def logout():
        logout_user()
        return redirect(url_for('core.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
        form = UpdateAccountForm()
        if form.validate_on_submit():
                if form.picture.data:
                        picture_file = save_picture(form.picture.data)
                        current_user.image_file = form.picture_file
                        # 로그인된 유저 사진을 업데이트
                current_user.username = form.username.data
                current_user.email = form.email.data
                db.session.commit()
                flash('Your account has been updated!', 'success')
                return redirect(url_for('users.account'))
        elif request.method == 'GET':
                form.username.data = current_user.username
                form.email.data = current_user.email
        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
        # 프로필 사진을 유저에게 받아서 파일속에 지정
        return render_template("account.html", image_file=image_file, form=form)



@users.route("/user/<string:username>")
# 여기서 지정한 username을 하단 def user_posts의 argument로 보낼 수 있음, string은 스트링값만 받겠다는것
def user_posts(username):
        page = request.args.get('page', 1, type=int)
        # page argument를 가져오는데 default를 1로 정하고 int만 받기로해서 int가 아니면 에러 
        user = User.query.filter_by(username=username).first_or_404()
        # 유저 목록중에 검색을 하고 값이 없으면 404에러 발생 
        posts = Post.query.filter_by(author=user)\
                .order_by(Post.date_posted.desc())\
                .paginate(page=page, per_page=5)
        # 줄을 바꿀때 \ 를 하면 코드를 이어지게 할 수 있음
        # paginate로 페이지를 생성, per_page는 각 페이지마다 있을 page를 지정, page는 위의 argument
        # order_by로 표시할 순서 지정, desc로 내림차순(최신이 먼저)
        return render_template('user_posts.html', posts=posts, user=user)





@users.route("/reset_password", methods=['GET', 'POST'])
# 로그인해야 접속할 수 있게 만들어줌
def reset_request():
        if current_user.is_authenticated:
                return redirect(url_for('core.home'))
                # 유저가 이미 로그인된 상태이면 접속하지 못하게 함
        form = ResetRequestForm()
        if form.validate_on_submit():
                user = User.query.filter_by(email=form.email.data).first()
                send_reset_email(user)
                flash('비밀번호 초기화를 위한 이메일이 전송되었습니다.', 'info')
                return redirect(url_for('users.login'))
        return render_template('reset_request.html', form=form)




@users.route("/reset_password/<token>", methods=['GET', 'POST'])
# 로그인해야 접속할 수 있게 만들어줌
def reset_password(token):
        if current_user.is_authenticated:
                return redirect(url_for('core.home'))
        user = User.verify_reset_token(token)
        if user is None:
                flash('유효하지 않거나 만료된 토큰입니다.', 'warning')
                return redirect(url_for('users.reset_request'))
        form = ResetPasswordForm()
        if form.validate_on_submit():
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                # 입력된 비밀번호를 해시값으로 저장함, decode utf-8은 해시값을 string으로 변환해줌
                user.password = hashed_password
                db.session.commit()
                # 유저의 비밀번호 변경 후, commit로 최종결정
                flash('비밀번호가 초기화 되었습니다! 변경된 비밀번호로 로그인 하실 수 있습니다.', 'success')
                return redirect(url_for('users.login'))
        return render_template('reset_password.html', form=form)