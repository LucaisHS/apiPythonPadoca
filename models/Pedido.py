from uuid import uuid4, UUID
from sqlalchemy.dialects.mysql import BINARY
from sqlalchemy import Column, String, Date, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship
from db.db import db
import enum

class PedidoEstado(enum.Enum):
    PENDENTE = "PENDENTE"
    PAGO = "PAGO"
    CANCELADO = "CANCELADO"
    ENTREGUE = "ENTREGUE"
    PREPARANDO_PEDIDO = "PREPARANDO_PEDIDO"
    SAINDO_ENTREGA = "SAINDO_ENTREGA"

class Pedido(db.Model):
    __tablename__ = 'pedido'

    pedido_id = Column(BINARY(16), primary_key=True, default=uuid4)
    data_pedido = Column(Date, nullable=False)
    valor_total = Column(Numeric(10, 2), nullable=False)
    pedido_estado = Column(Enum(PedidoEstado), nullable=False)

    # Relacionamento com Usuario
    usuario = db.relationship('Usuario', back_populates='pedidos')
    usuario_id = db.Column(db.String(36), db.ForeignKey('usuario.usuario_id'))

    produtos_pedido = relationship('ProdutoPedido', back_populates='pedido', lazy=True)
    #usuario = relationship('Usuario', backref='pedidos')

    def __init__(self, **kwargs):
        """
        Inicializa o Pedido com os dados fornecidos dinamicamente.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self):
        return {
            'pedido_id': str(UUID(bytes=self.pedido_id)),  # Converte bytes para UUID
            'data_pedido': self.data_pedido.strftime('%d/%m/%Y'),
            'valor_total': float(self.valor_total),  # Converte Decimal para float
            'pedido_estado': self.pedido_estado.value,  # Enum como string
            'usuario_id': str(UUID(bytes=self.usuario_id)),  # Converte bytes para UUID
        }
