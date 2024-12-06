from sqlalchemy import text, func
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

    @staticmethod
    def count_pedido_by_data_pedido_between(start_date, end_date):
        return db.session.query(func.count(Pedido.pedido_id)).filter(
            Pedido.data_pedido.between(start_date, end_date)
        ).scalar()

    @staticmethod
    def count():
        return db.session.query(func.count(Pedido.pedido_id)).scalar()

    @staticmethod
    def find_average_pedidos_per_usuario():
        query = text("""
                SELECT AVG(pedidos_por_usuario.total_pedidos)
                FROM (
                    SELECT usuario_id, COUNT(*) AS total_pedidos
                    FROM pedido
                    GROUP BY usuario_id
                ) AS pedidos_por_usuario
            """)
        result = db.session.execute(query).scalar()
        return result

    @staticmethod
    def find_horarios_by_data(data):
        query = text("""
                SELECT CAST(p.horario_pedido AS time) 
                FROM pedido p 
                WHERE p.data_pedido = :data AND p.horario_pedido IS NOT NULL
            """)
        result = db.session.execute(query, {"data": data}).fetchall()
        return [row[0] for row in result]

    @staticmethod
    def find_all_horarios():
        query = text("""
                SELECT CAST(p.horario_pedido AS time) 
                FROM pedido p 
                WHERE p.horario_pedido IS NOT NULL
            """)
        result = db.session.execute(query).fetchall()
        return [row[0] for row in result]

    @staticmethod
    def count_pedidos_by_forma_pagamento():
        result = db.session.query(
            Pedido.forma_pagamento, func.count(Pedido.pedido_id)
        ).group_by(Pedido.forma_pagamento).all()
        return result

    @staticmethod
    def count_pedidos_por_intervalo_de_valores():
        query = text("""
            SELECT 
                CASE 
                    WHEN valor_total BETWEEN 0 AND 10 THEN '0-10'
                    WHEN valor_total BETWEEN 11 AND 20 THEN '11-20'
                    WHEN valor_total BETWEEN 21 AND 50 THEN '21-50'
                    WHEN valor_total BETWEEN 51 AND 100 THEN '51-100'
                    WHEN valor_total BETWEEN 101 AND 250 THEN '101-250'
                    ELSE '>251'
                END AS intervalo,
                COUNT(*) AS quantidade
            FROM pedido
            GROUP BY intervalo
            ORDER BY MIN(valor_total)
        """)
        result = db.session.execute(query).fetchall()

        # Converte o resultado em uma lista de tuplas
        return [(row[0], row[1]) for row in result]

    @staticmethod
    def calcular_valor_medio_pedidos():
        return db.session.query(func.avg(Pedido.valor_total)).scalar()

    @staticmethod
    def buscar_pedido_de_maior_valor():
        subquery = db.session.query(func.max(Pedido.valor_total)).scalar_subquery()
        return db.session.query(Pedido).filter(Pedido.valor_total == subquery).first()

    @staticmethod
    def find_all_paginated(page, per_page):
        return db.session.query(Pedido).paginate(page=page, per_page=per_page, error_out=False)
