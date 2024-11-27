import datetime
from sqlalchemy import text
from db.db import db

class UsuarioRepository:

    @staticmethod
    def get_all():
        return Usuario.query.all()

    @staticmethod
    def find_by_id(usuario_id):
        return Usuario.query.get(usuario_id)

    @staticmethod
    def save(usuario):
        db.session.add(usuario)
        db.session.commit()

    @staticmethod
    def delete(usuario):
        db.session.delete(usuario)
        db.session.commit()

    @staticmethod
    def find_data_nascimento_between(start_date: datetime.date, end_date: datetime.date):
        query = text("""
                SELECT data_nascimento 
                FROM usuario 
                WHERE data_nascimento BETWEEN :startDate AND :endDate
            """)
        # Usa `mappings()` para retornar os resultados como dicionários
        result = db.session.execute(query, {"startDate": start_date, "endDate": end_date}).mappings()
        return [row["data_nascimento"] for row in result]
