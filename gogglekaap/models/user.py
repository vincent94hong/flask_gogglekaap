from gogglekaap import db
from sqlalchemy import func

class User(db.Model): # class = sql의 table
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20), unique=True, nullable=False)
    user_name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(600), nullable=False)
    created_at = db.Column(db.DateTime(), server_default=func.now()) 
    # server_default -> 해당 컬럼이 생성되기 이전의 파일에도 지금 시간으로 생성일자 작성
    # 그냥 default -> 추후 생성되는 데이터에 대해서만 적용.


    @classmethod
    def find_one_by_user_id(cls, user_id):
        return User.query.filter_by(user_id=user_id).first()