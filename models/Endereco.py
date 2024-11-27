from uuid import uuid4, UUID
from sqlalchemy.dialects.mysql import BINARY
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from db.db import db

class Endereco(db.Model):
    __tablename__ = 'endereco'

    endereco_id = Column(BINARY(16), primary_key=True, default=uuid4)
    rua = Column(String(255), nullable=False)
    numero = Column(String(10), nullable=False)
    bairro = Column(String(100), nullable=False)
    cidade = Column(String(100), nullable=False)
    cep = Column(String(20), nullable=False)
    complemento = Column(String(255), nullable=True)

    # Chave estrangeira
    usuario_id = Column(BINARY(16), ForeignKey('usuario.usuario_id'), nullable=False)

    def to_dict(self):
        return {
            'endereco_id': str(UUID(bytes=self.endereco_id)),  # Converte bytes para UUID
            'rua': self.rua,
            'numero': self.numero,
            'bairro': self.bairro,
            'cidade': self.cidade,
            'cep': self.cep,
            'complemento': self.complemento,
            'usuario_id': str(UUID(bytes=self.usuario_id)),  # Converte bytes para UUID
        }
