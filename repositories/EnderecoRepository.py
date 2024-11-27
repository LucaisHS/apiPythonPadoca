from models.Endereco import Endereco
from db.db import db

class EnderecoRepository:
    @staticmethod
    def get_all():
        return Endereco.query.all()

    @staticmethod
    def find_by_id(endereco_id):
        return Endereco.query.get(endereco_id)

    @staticmethod
    def find_by_usuario_id(usuario_id):
        return Endereco.query.filter_by(usuario_id=usuario_id).all()

    @staticmethod
    def save(endereco):
        db.session.add(endereco)
        db.session.commit()

    @staticmethod
    def delete(endereco):
        db.session.delete(endereco)
        db.session.commit()
