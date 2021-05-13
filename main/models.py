from main import db, login_manger, app
# from main은 main폴더 내 __init__.py로 진입함
from datetime import datetime
# 현재시간 불러와줌
# pip install datetime 해야함!!
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer




@login_manger.user_loader
def load_user(user_id):
        return User.query.get(int(user_id))
        # 유저 아이디를 사용해서 유저의 모든 정보를 찾아줌


class User(db.Model, UserMixin):
        # UserMixin으로 유저의 현재 상태 알려줌
        id = db.Column(db.Integer, primary_key=True)
        # primary_key는 id가 고유의 것임을 나타내줌
        username = db.Column(db.String(20), unique=True, nullable=False)
        # String의 최대길이 20이여서 20을 넣고 unique는 고유의 것임을 의미하고 nullable은 빈값이면 안된다는 것 
        email = db.Column(db.String(120), unique=True, nullable=False)
        image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
        password = db.Column(db.String(60), nullable=False)
        posts = db.relationship('Post', backref='author', lazy=True)
        # relationship은 Post 모델과 관계가 있음을 알려주고 backref을 사용해서 author라는 Column을 Post에서 사용할 수 있게 만듬, lazy는 데이터를 모두 로드하고 보낸다는 의미
        # 여기서 Post는 아래 Class에서 설정한 모델이름 Post임
        
        def get_reset_token(self, expire_sec=600):
                s = Serializer(app.config['SECRET_KEY'], expire_sec)
                # Serializer(secret key, 만료하는 시간(초단위))
                return s.dumps({'user_id': self.id}).decode('utf-8')
                # dumps를 통해 key생성, 유저의 고유 아이디를 전송, utf-8로 decode


        @staticmethod
        # 파이썬에게 self를 arg로 안쓰고 token만 쓰겠다고 말해줌
        def verify_reset_token(token):
                s = Serializer(app.config['SECRET_KEY'])
                try:
                        user_id = s.loads(token)['user_id']
                        # loads로 토큰의 유저 아이디를 불러옴
                except:
                        return None
                        # 토큰 유효X하면 None 반환
                return User.query.get(user_id)
                # 토큰이 유효하면 유저아이디 반환


        def __repr__(self):
                return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(100), nullable=False)
        date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
        # datetime.utcnow를 argument 형태로 전송하기 위해서 ()를 안 적는것임
        content = db.Column(db.Text, nullable=False)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        # ForeignKey는 외부 모델에서 불러올때 사용, user모델에서 소문자인 이유는 실제 데이터에서 불러오는데, 실제 데이터에서는 모두 소문자이기 때문

        def __repr__(self):
                return f"Post('{self.title}', '{self.date_posted}')"