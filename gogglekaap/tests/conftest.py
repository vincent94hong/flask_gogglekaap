import sys, os
sys.path.append('.')
import pytest

from gogglekaap import create_app, db
from gogglekaap.configs import TestingConfig
from gogglekaap.models.user import User as UserModel
from gogglekaap.models.memo import Memo as MemoModel

@pytest.fixture(scope='session')
def user_data():
    yield dict(
        user_id='tester', 
        user_name='tester',
        password='tester'
    )


@pytest.fixture(scope='session')
def memo_data():
    yield dict(
        title = 'title',
        content = 'content'
    )


@pytest.fixture(scope='session')
def app(user_data, memo_data):
    app = create_app(TestingConfig())
    with app.app_context():
        db.drop_all()
        db.create_all()
        user = UserModel(**user_data)
        db.session.add(user)
        db.session.flush() # commit 과 비슷한 기능, 실제 커밋은 아님. user의 데이터가 필요하기 때문에 커밋과 유사한 상태를 만듦.
        memo_data['user_id'] = user.id # 커밋이 된 상태어야 user의 데이터를 가져와서 user.id를 가져옴
        db.session.add(MemoModel(**memo_data))
        db.session.commit()
        yield app
        # 불필요 디비 정리 (sqlite_test.db)
        db.drop_all()
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace(
            'sqlite:///',
            ''
        )
        if os.path.isfile(db_path):
            os.remove(db_path)


@pytest.fixture(scope='session')
def client(app, user_data):
    with app.test_client() as client:
        # NOTE: 세션 입혀주기
        with client.session_transaction() as session:
            session['user_id'] = user_data.get('user_id')
        yield client