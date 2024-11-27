from sqlalchemy import text
from sqlalchemy.orm import load_only
from models.Pedido import Pedido
from db.db import db

class PedidoRepository:
    @staticmethod
    def find_all_by_usuario_id(usuario_id_bin, page, per_page):
        """
        Retorna todos os pedidos de um usuário com paginação.
        """
        return Pedido.query.filter_by(usuario_id=usuario_id_bin).paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def find_by_pedido_id(pedido_id_bin):
        """
        Retorna um pedido específico pelo ID.
        """
        return Pedido.query.filter_by(pedido_id=pedido_id_bin).first()
    @staticmethod
    def save(pedido):
        """
        Salva um novo pedido ou atualiza um existente.
        """
        db.session.add(pedido)
        db.session.commit()

    @staticmethod
    def delete(pedido):
        """
        Deleta um pedido específico.
        """
        db.session.delete(pedido)
        db.session.commit()
