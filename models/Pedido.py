from uuid import uuid4, UUID
from sqlalchemy.dialects.mysql import BINARY
from sqlalchemy import Column, String, Date, ForeignKey, Numeric, Enum, Time
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


class FormaPagamento(enum.Enum):
    DEBITO = "DEBITO"
    CREDITO = "CREDITO"
    PIX = "PIX"
    DINHEIRO = "DINHEIRO"


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

    forma_pagamento = Column(Enum(FormaPagamento), nullable=False)
    horario_pedido = Column(Time, nullable=False)
    horario_entrega = Column(Time, nullable=False)

    def __init__(self, **kwargs):
        """
        Inicializa o Pedido com os dados fornecidos dinamicamente.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self):
        return {
            'pedidoId': str(UUID(bytes=self.pedido_id)),  # Converte bytes para UUID
            'dataPedido': self.data_pedido.strftime('%d/%m/%Y'),
            'valorTotal': float(self.valor_total),  # Converte Decimal para float
            'pedidoEstado': self.pedido_estado.value,  # Enum como string
            'usuario_id': str(UUID(bytes=self.usuario_id)),  # Converte bytes para UUID
            'formaPagamento': self.forma_pagamento.name if self.forma_pagamento else None,
            'horarioPedido': self.horario_pedido.strftime('%H:%M:%S') if self.horario_pedido else None,
            'horarioEntrega': self.horario_entrega.strftime('%H:%M:%S') if self.horario_entrega else None,
        }
