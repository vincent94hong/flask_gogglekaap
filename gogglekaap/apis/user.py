from flask import g
from flask_restx import Namespace, Resource, fields, reqparse
from gogglekaap.models.user import User as UserModel
from werkzeug import security


ns = Namespace(
    'users',
    description='유저 관련 API'
)


user = ns.model('User',{
    'id': fields.Integer(required=True, description='유저 고유 번호'),
    'user_id': fields.String(required=True, description='유저 아이디'),
    'user_name': fields.String(required=True, description='유저 이름'),
    'created_at': fields.DateTime(description='유저 가입 일자')
})


post_parser = reqparse.RequestParser()
post_parser.add_argument('user_id', required=True, help='유저 고유 아이디')
post_parser.add_argument('user_name', required=True, help='유저 이름')
post_parser.add_argument('password', required=True, help='유저 패스워드')


# /api/users
@ns.route('')
@ns.response(409, 'User Id is already exists.')
@ns.deprecated
class UserList(Resource):

    # skip_none=True -> 특정 field가 none일 때는 아에 key값을 만들지 않음.
    # 예를들어 user_name이 없다면, 데이터는 {id, user_id}만 가지게 됨.
    # skip_none=False -> {id, user_id, user_name=null} 형태로 만들어질 것.
    @ns.marshal_list_with(user, skip_none=True)
    def get(self):
        '''유저 복수 조회'''
        data = UserModel.query.all()
        return data
    
    @ns.expect(post_parser)
    @ns.marshal_list_with(user, skip_none=True)
    def post(self):
        '''유저 생성'''
        args = post_parser.parse_args()
        user_id = args['user_id']
        user = UserModel.find_one_by_user_id(user_id)
        if user:
            ns.abort(409) # 이미 있는 아이디임을 알려줌.
        user = UserModel(
            user_id = user_id,
            user_name = args['user_name'],
            password = security.generate_password_hash(args['password'])
        )
        g.db.add(user)
        g.db.commit()
        return user, 201 # 201 -> create 되었다.


# /api/users/1 -> id 1인 user get
@ns.route('/<int:id>')
@ns.param('id', '유저 고유 번호')
@ns.deprecated
class User(Resource):
    @ns.marshal_list_with(user, skip_none=True)
    def get(self, id):
        '''유저 단수 조회'''
        data = UserModel.query.get_or_404(id)
        return data
    