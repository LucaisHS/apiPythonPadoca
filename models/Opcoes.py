from uuid import uuid4, UUID
from sqlalchemy.dialects.mysql import BINARY
from sqlalchemy import Column, String, Numeric
from sqlalchemy.orm import relationship
from db.db import db
from models.Produto import produto_opcoes  # Importa a tabela associativa para Many-to-Many

class Opcoes(db.Model):
    __tablename__ = 'opcoes'

    opcao_id = Column(BINARY(16), primary_key=True, default=uuid4)
    nome = Column(String(100), nullable=False)
    preco_add = Column(Numeric(10, 2), nullable=False)

    # Relacionamento Many-to-Many com Produto
    produtos = relationship(
        'Produto',
        secondary=produto_opcoes,
        back_populates='opcoes',
        lazy=True
    )

    produtos_pedido = relationship('ProdutoPedido', back_populates='opcoes', lazy=True)

    def to_dict(self):
        return {
            'opcao_id': str(UUID(bytes=self.opcao_id)),  # Converte bytes para UUID
            'nome': self.nome,
            'preco_add': float(self.preco_add)  # Converte Decimal para float
        }
