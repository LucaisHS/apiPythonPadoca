from models.ProdutoPedido import ProdutoPedido
from db.db import db

class ProdutoPedidoRepository:
    @staticmethod
    def find_all_by_pedido_id(pedido_id):
        """
        Retorna todos os ProdutoPedido associados a um pedido específico.
        """
        return ProdutoPedido.query.filter_by(pp_pedido_id=pedido_id).all()

    @staticmethod
    def save(produto_pedido):
        """
        Salva um novo ProdutoPedido ou atualiza um existente.
        """
        db.session.add(produto_pedido)
        db.session.commit()

    @staticmethod
    def delete(produto_pedido):
        """
        Deleta um ProdutoPedido específico.
        """
        db.session.delete(produto_pedido)
        db.session.commit()
