from models.Opcoes import Opcoes
from db.db import db
from sqlalchemy.sql import text

class OpcoesRepository:
    @staticmethod
    def find_all_by_produto_id(produto_id_bin):
        """
        Retorna todas as opções relacionadas a um produto específico.
        """
        query = text("""
            SELECT o.* FROM opcoes o
            JOIN produtosOpcoes po ON o.opcao_id = po.opcao_id
            WHERE po.produto_id = :produto_id
        """)
        result = db.session.execute(query, {'produto_id': produto_id_bin})
        rows = result.mappings().all()
        return [Opcoes(**row) for row in rows]

    @staticmethod
    def find_opcoes_by_opcao_id(opcao_id_bin):
        """
        Retorna uma opção específica pelo ID.
        """
        return Opcoes.query.filter_by(opcao_id=opcao_id_bin).first()

    @staticmethod
    def save(opcao):
        """
        Salva uma nova opção ou atualiza uma existente.
        """
        db.session.add(opcao)
        db.session.commit()

    @staticmethod
    def delete(opcao):
        """
        Deleta uma opção específica.
        """
        db.session.delete(opcao)
        db.session.commit()
