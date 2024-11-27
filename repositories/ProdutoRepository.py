from models.Produto import Produto
from db.db import db
from sqlalchemy.sql import text

class ProdutoRepository:
    @staticmethod
    def find_produto_by_nome(nome):
        """
        Retorna um produto específico pelo nome.
        """
        return Produto.query.filter_by(nome=nome).first()

    @staticmethod
    def find_produto_by_produto_id(produto_id_bin):
        """
        Retorna um produto específico pelo ID.
        """
        return Produto.query.filter_by(produto_id=produto_id_bin).first()

    @staticmethod
    def find_all(page=None, per_page=None):
        """
        Retorna todos os produtos com ou sem paginação.
        """
        if page and per_page:
            return Produto.query.paginate(page=page, per_page=per_page, error_out=False)
        return Produto.query.all()

    @staticmethod
    def find_all_ids():
        """
        Retorna todos os IDs dos produtos.
        """
        query = text("SELECT produto_id FROM produto")
        result = db.session.execute(query)
        return [row[0] for row in result.fetchall()]

    @staticmethod
    def save(produto):
        """
        Salva um novo produto ou atualiza um existente.
        """
        db.session.add(produto)
        db.session.commit()

    @staticmethod
    def delete(produto):
        """
        Deleta um produto específico.
        """
        db.session.delete(produto)
        db.session.commit()
