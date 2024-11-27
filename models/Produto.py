from uuid import uuid4, UUID
from sqlalchemy.dialects.mysql import BINARY
from sqlalchemy import Column, String, Numeric, Integer
from sqlalchemy.orm import relationship
from db.db import db

# Tabela associativa para Many-to-Many
produto_opcoes = db.Table(
    'produtos_opcoes',
    db.Column('produto_id', BINARY(16), db.ForeignKey('produto.produto_id'), primary_key=True),
    db.Column('opcoes_id', BINARY(16), db.ForeignKey('opcoes.opcao_id'), primary_key=True)
)

class Produto(db.Model):
    __tablename__ = 'produto'

    produto_id = Column(BINARY(16), primary_key=True, default=uuid4)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(255), nullable=True)
    preco = Column(Numeric(10, 2), nullable=False)
    estoque = Column(Integer, nullable=False)
    categoria = Column(String(50), nullable=True)
    imagem_url = Column(String(255), nullable=True)

    # Relacionamento Many-to-Many com Opcoes
    opcoes = relationship(
        'Opcoes',
        secondary=produto_opcoes,
        back_populates='produtos',
        lazy=True
    )

    produtos_pedido = relationship('ProdutoPedido', back_populates='produto', lazy=True)

    def to_dict(self):
        return {
            'produto_id': str(UUID(bytes=self.produto_id)),  # Converte bytes para UUID
            'nome': self.nome,
            'descricao': self.descricao,
            'preco': float(self.preco),  # Converte Decimal para float
            'estoque': self.estoque,
            'categoria': self.categoria,
            'imagem_url': self.imagem_url,
            'opcoes': [opcao.to_dict() for opcao in self.opcoes]  # Lista de opcoes relacionadas
        }
