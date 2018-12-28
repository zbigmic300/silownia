from api.config import db, ma
from api.db_lib.model import Deletable


class RevokedToken(db.Model, Deletable):
    __tablename__ = 'revoked_tokens'

    id = db.Column(db.Integer, db.Sequence('seq_revoked_tokens_id'), primary_key=True)
    jti = db.Column(db.String(255), nullable=False)
    expire_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<RevokedToken %s>' % self.jti


class RevokedTokenSchema(ma.ModelSchema):
    class Meta:
        model = RevokedToken
        sqla_session = db.session
