from flask import Flask
# from main.news_extracter import head_text_extracter
# from main.link_extracter import link_extracter
# from main.image_extracter import image_scr_extracter
from flask_sqlalchemy import SQLAlchemy
# pip install flask-sqlalchemy 해야함!!
from flask_bcrypt import Bcrypt
# pip install flask-bcrypt 해야함!!
from flask_login import LoginManager
# pip install flask-login 해야함!!
from flask_mail import Mail
# pip install flask-mail 해야함!!

import os
_basedir = os.path.abspath(os.path.dirname(__file__))
# 스크립트가 실행되는 경로 지정!!


# # EXTRACTOR
# #변수명 PNHL = paper_Name_HeadLine
# PNHL = head_text_extracter()
# links_list = link_extracter()
# img_scrs = image_scr_extracter()

# for pnhl,link,image_scr in zip(PNHL, links_list, img_scrs):
#         pnhl["url"] = link
#         pnhl["img_scr"] = image_scr

pnhl = [
        {'paper': '미디어', 'headline': '[유럽언론 톺아보기] ‘프렌치 폭스뉴스’ 대안이 된 미디어바우처', 'url': 'https://www.mediatoday.co.kr//news/articleView.html?idxno=213244', 'scr': 'https://www.mediatoday.co.kr//news/photo/202105/213244_336347_228.jpg'},
        {'paper': '한겨례', 'headline': '병아리색 민방위복 잘 어울리는 대선주자 정세균의 ‘도전’', 'url': 'https://www.hani.co.kr//arti/politics/polibar/994380.html?_fr=mt1', 'scr': 'http://flexible.img.hani.co.kr/flexible/normal/577/231/imgdb/child/2021/0509/52_16205263982809_20210402500505.jpg'}, 
        {'paper': '경향', 'headline': '미세먼지 걷힌 반가운 파란 하늘', 'url': 'http://photo.khan.co.kr/photo_view.html?artid=202105091247001&code=940100&slide=n&med_id=khan&type=news', 'scr': 'http://img.khan.co.kr/spko/ranking/2900/290003/20210509130203_29000302.jpg'}, 
        {'paper': '서울', 'headline': '“골든 건은 네 잘못”…故 손정민에게 큰절한 친구', 'url': 'https://www.seoul.co.kr//news/newsView.php?id=20210509500012', 'scr': 'https://img.seoul.co.kr/img/upload/2021/05/07/SSI_20210507204202_O2.jpg'}, 
        {'paper': '한국', 'headline': ' \'도자기 반입\' 박준영 "처벌될수도" 해석에 여권 고심 더 커진다', 'url': 'https://www.hankookilbo.com//News/Read/A2021050813370001283', 'scr': 'https://newsimg.hankookilbo.com/cms/articlerelease/2021/05/09/87d4509c-40bf-4d40-856f-ee5f44b8770e.jpg'}, 
        {'paper': '조선', 'headline': '[단독] 월 자문료 2900만원… 김오수, 로펌서 전관예우 특혜', 'url': 'https://www.chosun.com//national/court_law/2021/05/09/IP4AFRYTHFGWFNLQOXJ5TYB6VY/', 'scr': 'https://search.pstatic.net/common/?src=https%3A%2F%2Fimgnews.pstatic.net%2Fimage%2Forigin%2F023%2F2021%2F05%2F09%2F3612871.jpg&type=ff264_180&expire=2&refresh=true'},
        {'paper': '중앙', 'headline': "그 의원에 그 보좌관···의원들 때린 '조응천 그림자'", 'url': 'https://news.joins.com/article/24053021?cloc=joongang-home-toptype1basic', 'scr': 'https://wimage.joins.com/indexedit/joongang/202105/09/wimg_2021050910352217753.jpg'}, 
        {'paper': '뉴욕', 'headline': 'States Turn Down Hundreds of Thousands of Vaccine Doses as Demand Dips', 'url': 'https://www.nytimes.com/live/2021/05/08/world/covid-vaccine-coronavirus-cases/', 'scr': 'https://static01.nyt.com/images/2021/05/07/world/08hp-india-crematories-2-copy/08hp-india-crematories-2-copy-master1050-v3.jpg'},
        {'paper': '월스', 'headline': 'Bo, the Obama Family Dog Who Roamed White House, Dies ', 'url': 'https://www.wsj.com/articles/bo-the-obama-family-dog-who-roamed-white-house-dies-11620528154?mod=latest_headlines', 'scr': 'https://images.wsj.net/im-336038?width=100&height=67'}
]


# FLASK APP
app = Flask("__name__", template_folder='main/templates', static_folder='main/static')
# 템플릿하고 스태틱이 404가 떠서 여기서 지정해줘야함(앱형식으로 배포할때)


# SECRET KEY
app.config['SECRET_KEY'] = 'e96e92010ed981ce85ab2289ed302600'

# SQLAlchemy track 변경 방지
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQL DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(_basedir, 'site.db')
# ///는 현재 경로를 의미함 -> site.db가 현재 폴더에 생성됨
db = SQLAlchemy(app)


bcrypt = Bcrypt(app)
# 해시값 생성용

login_manger = LoginManager(app)
login_manger.login_view = 'users.login'
# 유저를 login페이지로 이동시킴 url_for과 유사, 괄호 속 값이 
login_manger.login_message_category = 'info'
# 안내창 형식을 지정함


# EMAIL CONFIGURATION
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)

from main.users.routes import users
from main.posts.routes import posts
from main.core.routes import core
# 에러나는 것을 방지하기 위해 아래에다가 놓음 -> routes를 import하면 실행하게 되는데, routes에 적어놓은 app을 인식하기 위해서는 app을 정의한 이후에 import해야함

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(core)