from flask import Blueprint, g, abort
from flask_restx import Api
from .user import ns as UserNamespace
from .memo import ns as MemoNamespace
from functools import wraps


def check_session(func):
    @wraps(func)
    def __wrapper(*args, **kwargs):
        if not g.user:
            abort(401) # 인증되지 않은 유저
        return func(*args, **kwargs)
    return __wrapper


blueprint = Blueprint(
    'api',
    __name__,
    url_prefix='/api'
)

api = Api(
    blueprint,
    title='Goggle kaap API',
    version='1.0',
    doc='/docs',
    decorators=[check_session],
    description='Welcome my api docs'
)

api.add_namespace(UserNamespace)
api.add_namespace(MemoNamespace)