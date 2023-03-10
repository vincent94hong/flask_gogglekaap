from flask import Flask, g
from flask import render_template
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()

def create_app(config=None):
    app = Flask(__name__)


    '''Flask Configs'''
    from .configs import DevelopmentConfig, ProductionConfig
    # app.config['SECRET_KEY'] = 'secretkey' # 개발자모드-어플리케이션-쿠키에 session 이라는 이름에, 암호화된 데이터로 저장됨.
    # app.config['SESSION_COOKIE_NAME'] = 'gogglekaap' # session 이라는 이름을 gogglekaap 으로 변경. 암호화 데이터는 그대로.
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/gogglekaap?charset=utf8'
    # # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # SQLALCHEMY_TRACK_MODIFICATIONS 에러발생시 설정.
    # app.config['SWAGGER_UI_DOC_EXPANSION'] = 'list'

    # 현재는 그냥 자동적으로 refresh 되는 듯.
    # if app.config['DEBUG']: # 기존에는 css 파일 등의 캐시가 기본적으로 10시간 지속되어 새로고침을 해도 변경이 적용되지 않고 이전 상태가 유지.
    #     app.config['SEND_FIND_MAX_DEFAULT'] = 1 # 개발자 모드의 debug를 1초마다 refresh 시키는 것. -> chrome 개발자모드 network 에서 style.css 파일의 headers, Cashe-Control: public, max-age=43200 -> 1로 변경하는 것.
    #     app.config['WTF_CSRF_ENABLED'] = False # user post api 설계시 csrf 설정을 아직 안했지만 결과를 실험해보기 위해, 개발자모드에서 설정을 꺼놓는 것.

    if not config:
        if app.config['DEBUG']:
            config = DevelopmentConfig()
        else:
            config = ProductionConfig()

    print('run with:', config)
    app.config.from_object(config) # config 호출

    
    '''CSRF INIT'''
    csrf.init_app(app)


    '''DB INIT'''
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)


    '''Routes INIT'''
    from gogglekaap.routes import base_route, auth_route
    app.register_blueprint(base_route.bp)
    app.register_blueprint(auth_route.bp)


    '''Restx INIT'''
    from gogglekaap.apis import blueprint as api
    app.register_blueprint(api)    


    '''REQUEST HOOK'''
    @app.before_request
    def before_request():
        g.db = db.session
    
    @app.teardown_request
    def teardown_request(exception):
        if hasattr(g, 'db'):
            g.db.close()

    @app.errorhandler(404)
    def page_404(error):
        return render_template('/404.html'), 404

    return app