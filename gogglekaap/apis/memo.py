from gogglekaap.models.memo import Memo as MemoModel
from gogglekaap.models.user import User as UserModel
from flask_restx import Namespace, fields, Resource, reqparse, inputs
from flask import g, current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import os
import shutil

ns = Namespace(
    'memos',
    description='메모 관련 API'
)


memo = ns.model('Memo', {
    'id': fields.Integer(required=True, description='메모 고유 아이디'),
    'user_id': fields.Integer(required=True, description='유저 고유 아이디'),
    'title': fields.String(required=True, description='메모 제목'),
    'content': fields.String(required=True, description='메모 내용'),
    'linked_image': fields.String(required=False, description='메모 이미지 경로'),
    'is_deleted': fields.Boolean(description='메모 삭제 상태'),
    'created_at': fields.DateTime(description='메모 작성일'),
    'updated_at': fields.DateTime(description='메모 변경일'),
})


parser = reqparse.RequestParser()
parser.add_argument('title', required=True, help='메모 제목')
parser.add_argument('content', required=True, help='메모 내용')
parser.add_argument('linked_image', location='files', required=False, type=FileStorage, help='메모 이미지')
parser.add_argument('is_deleted', required=False, type=inputs.boolean, help='메모 삭제 상태')


put_parser = parser.copy()
put_parser.replace_argument('title', required=False, help='메모 제목')
put_parser.replace_argument('content', required=False, help='메모 내용')


get_parser = reqparse.RequestParser()
get_parser.add_argument('page', required=False, type=int, help='메모 페이지 번호')
get_parser.add_argument('needle', required=False, help='메모 검색어')
get_parser.add_argument('is_deleted', required=False, type=inputs.boolean, help='메모 삭제 상태')


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in {
            'png', 
            'jpg', 
            'jpeg', 
            'gif'
        }


def randomword(length):
    import random, string
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def save_file(file):
    if file.filename == '':
        ns.abort(400)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # ../../test.jpg -> test.jpg 로 변경해줌. (띄어쓰기는 언더스코어 처리)

        relative_path = os.path.join(
            current_app.static_url_path[1:], # /static -> static
            current_app.config['USER_STATIC_BASE_DIR'], # static/user_images
            g.user.user_id, # static/user_images/{user_id}
            'memos', # static/user_images/{user_id}/memos
            randomword(5), # static/user_images/{user_id}/memos/asdfg
            filename # static/user_images/{user_id}/memos/asdfg/{filename}
        )

        upload_path = os.path.join(
            current_app.root_path,
            relative_path
        )

        os.makedirs(
            os.path.dirname(upload_path),
            exist_ok=True # 폴더가 이미 존재해도 에러를 노출시키지 마.
        )
        file.save(upload_path)
        return relative_path, upload_path
    else:
        ns.abort(400)


@ns.route('')
class MemoList(Resource):
    
    @ns.marshal_list_with(memo, skip_none=True)
    @ns.expect(get_parser)
    def get(self):
        '''메모 복수 조회'''
        args = get_parser.parse_args()
        page = args['page']
        needle = args['needle']
        is_deleted = args['is_deleted']
        if is_deleted is None:
            is_deleted = False
        per_page = 15 # page 마다 갯수를 15개

        base_query = MemoModel.query.join(
            UserModel,
            UserModel.id == MemoModel.user_id
        ).filter(
            UserModel.id == g.user.id,
            MemoModel.is_deleted == is_deleted
        )

        if needle:
            needle = f'%{needle}%'
            base_query = base_query.filter(
                MemoModel.title.ilike(needle)|MemoModel.content.ilike(needle)
            )

        pages = base_query.order_by(
            MemoModel.created_at.desc()
        ).paginate(
            page=page,
            per_page=per_page
        )
        return pages.items
    
    
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
        if args['is_deleted'] is not None:
            memo.is_deleted = args['is_deleted']
        file = args['linked_image']
        if file:
            relative_path, _ = save_file(file) # _ : upload_path 안쓰기때문에 _(under bar)처리 해놓음
            memo.linked_image = relative_path
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
        if args['is_deleted'] is not None:
            memo.is_deleted = args['is_deleted']
        file = args['linked_image']
        if file:
            relative_path, upload_path = save_file(file)
            if memo.linked_image:
                origin_path = os.path.join(
                    current_app.root_path,
                    memo.linked_image
                )
                if origin_path != upload_path:
                    if os.path.isfile(origin_path):
                        shutil.rmtree(os.path.dirname(origin_path))
            memo.linked_image = relative_path
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
    

@ns.param('id', '메모 고유 아이디')
@ns.route('/<int:id>/image')
class MemoImage(Resource):

    def delete(self, id):
        '''메모 이미지 삭제'''
        memo = MemoModel.query.get_or_404(id)
        if g.user.id != memo.user_id:
            ns.abort(403)
        if memo.linked_image:
            origin_path = os.path.join(
                current_app.root_path,
                memo.linked_image
            )
            if os.path.isfile(origin_path):
                shutil.rmtree(os.path.dirname(origin_path))
            memo.linked_image = None
            g.db.commit()
        return '', 204