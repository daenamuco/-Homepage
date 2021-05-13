import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from main import app, mail



def save_picture(form_picture):
        random_hex = secrets.token_hex(8)
        # secrets로 랜덤 해쉬값 생성(8자리)
        _, f_ext = os.path.splitext(form_picture.filename)
        # _는 쓰지 않는 변수값을 나타낼 때 사용(변수 사용안했다는 에러방지 위함), splitext로 확장자와 파일명 분리
        picture_filename = random_hex + f_ext
        # 해쉬값과 확장자 합침
        picture_path = os.path.join(app.root_path, 'static/profile_pics', 'picture_filename')
        # os.path.join으로 파일 경로와 이름을 하나로 생성
        output_size = (125, 125)
        # crop할 size를 정함
        i = Image.open(form_picture)
        i.thumbnail(output_size)
        i.save(picture_path)
        # 새롭게 생성된 경로에 crop된 사진을 저장함
        
        return picture_filename



def send_reset_email(user):
        token = user.get_reset_token()
        # User 모델 내 토큰 불러오는 함수
        msg = Message('비밀번호 초기화 요청', sender='daenamu_noreply@google.com', recipients=[user.email])
        # Message(이메일 제목, sender=보내는 사람, recipients=리스트 형식으로 여러명에게 보낼 수 있지만 한명에게만 보냄)
        msg.body = f'''비밀번호 초기화를 위한 링크입니다: {url_for('users.reset_password', token=token, _external=True)}

링크는 10분 뒤 자동으로 만료됩니다.
'''
# .body는 이메일 내용 설정하는 부분, 이메일이 길어지면 Jinja2로 작성하는 방법도 있다!!
# _external True를 하면 url 자체를 글자 그대로 전송함, 안쓰면 기존 코드 내에서 사용하는 relative url을 전송하여 에러가 남 
        mail.send(msg)
        # 이메일을 전송함!!