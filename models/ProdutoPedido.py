from uuid import uuid4, UUID

from sqlalchemy import Column, ForeignKey, Numeric, Integer, BINARY
from sqlalchemy.orm import relationship
from db.db import db

class ProdutoPedido(db.Model):
    __tablename__ = 'produto_pedido'

    produto_pedido_id = Column(BINARY(16), primary_key=True, default=uuid4)
    pp_pedido_id = Column(BINARY(16), ForeignKey('pedido.pedido_id'), nullable=False)
    pp_produto_id = Column(BINARY(16), ForeignKey('produto.produto_id'), nullable=False)
    pp_opcao_id = Column(BINARY(16), ForeignKey('opcoes.opcao_id'), nullable=True)

    desconto = Column(Numeric(10, 2), nullable=True)
    preco_unidade = Column(Numeric(10, 2), nullable=False)
    quantidade = Column(Integer, nullable=False)

    # Relacionamentos
    pedido = relationship('Pedido', back_populates='produtos_pedido')
    produto = relationship('Produto', back_populates='produtos_pedido')
    opcoes = relationship('Opcoes', back_populates='produtos_pedido')  # Relacionamento com Opcoes

    def to_dict(self):
        return {
            'produto_pedido_id': str(UUID(bytes=self.produto_pedido_id)),
            'pedido_id': str(UUID(bytes=self.pp_pedido_id)),
            'produto_id': str(UUID(bytes=self.pp_produto_id)) if self.pp_produto_id else None,
            'opcao_id': str(UUID(bytes=self.pp_opcao_id)) if self.pp_opcao_id else None, # talvez seja aqui
            'quantidade': self.quantidade,
            'preco_unidade': float(self.preco_unidade),
            'desconto': float(self.desconto) if self.desconto else None,
        }
