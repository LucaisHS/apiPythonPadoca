from uuid import uuid4, UUID
from sqlalchemy.dialects.mysql import BINARY
from sqlalchemy import Column, String, Date, LargeBinary
from sqlalchemy.orm import relationship
from db.db import db
from models.Endereco import Endereco
from models.Pedido import Pedido

class Usuario(db.Model):
    __tablename__ = 'usuario'

    usuario_id = Column(BINARY(16), primary_key=True, default=uuid4)
    nome = Column(String(50))
    sobrenome = Column(String(50))
    senha = Column(String(255))
    telefone = Column(String(20))
    email = Column(String(100))
    data_nascimento = Column(Date)

    # Relacionamentos
    #1 pra n
    enderecos = relationship('Endereco', backref='usuario', lazy=True)
    pedidos = relationship('Pedido', back_populates='usuario', lazy=True)

    def to_dict(self):
        return {
            'usuario_id': str(UUID(bytes=self.usuario_id)),  # Converte bytes para UUID
            'nome': self.nome,
            'sobrenome': self.sobrenome,
            'telefone': self.telefone,
            'email': self.email,
        }
