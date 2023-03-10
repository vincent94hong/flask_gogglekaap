from gogglekaap.models.memo import Memo as MemoModel
from gogglekaap.models.user import User as UserModel
from flask_restx import Namespace, fields, Resource, reqparse
from flask import g

ns = Namespace(
    'memos',
    description='메모 관련 API'
)


memo = ns.model('Memo', {
    'id': fields.Integer(required=True, description='메모 고유 아이디'),
    'user_id': fields.Integer(required=True, description='유저 고유 아이디'),
    'title': fields.String(required=True, description='메모 제목'),
    'content': fields.String(required=True, description='메모 내용'),
    'created_at': fields.DateTime(description='메모 작성일'),
    'updated_at': fields.DateTime(description='메모 변경일'),
})


parser = reqparse.RequestParser()
parser.add_argument('title', required=True, help='메모 제목')
parser.add_argument('content', required=True, help='메모 내용')


put_parser = parser.copy()
put_parser.replace_argument('title', required=False, help='메모 제목')
put_parser.replace_argument('content', required=False, help='메모 내용')


@ns.route('')
class MemoList(Resource):
    
    @ns.marshal_list_with(memo, skip_none=True)
    def get(self):
        '''메모 복수 조회'''
        data = MemoModel.query.join(
            UserModel,
            UserModel.id == MemoModel.user_id
        ).filter(
            UserModel.id == g.user.id
        ).order_by(
            MemoModel.created_at.desc() # 최근인 순서로 order
        ).limit(10).all() # 테스트용으로 10개만.
        return data
    
    
    @ns.expect(parser)
    @ns.marshal_list_with(memo, skip_none=True)
    def post(self):
        '''메모 생성'''
        args = parser.parse_args()
        memo = MemoModel(
            title = args['title'],
            content = args['content'],
            user_id = g.user.id
        )
        g.db.add(memo)
        g.db.commit()
        return memo, 201
    

@ns.param('id', '메모 고유 아이디')
@ns.route('/<int:id>')
class Memo(Resource):
    
    @ns.marshal_list_with(memo, skip_none=True)
    def get(self, id):
        '''메모 단수 조회'''
        memo = MemoModel.query.get_or_404(id)
        if g.user.id != memo.user_id:
            ns.abort(403)
        return memo

    
    @ns.expect(put_parser)
    @ns.marshal_list_with(memo, skip_none=True)
    def put(self, id):
        '''메모 업데이트'''
        args = put_parser.parse_args()
        memo = MemoModel.query.get_or_404(id)
        if g.user.id != memo.user_id:
            ns.abort(403)
        if args['title'] is not None:
            memo.title = args['title']
        if args['content'] is not None:
            memo.content = args['content']
        g.db.commit()
        return memo
        
    
    def delete(self, id):
        '''메모 삭제'''
        memo = MemoModel.query.get_or_404(id)
        if g.user.id != memo.user_id:
            ns.abort(403)
        g.db.delete(memo)
        g.db.commit()
        return '', 204