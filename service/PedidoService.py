from repositories.PedidoRepository import PedidoRepository
from repositories.UsuarioRepository import UsuarioRepository
from models.Pedido import Pedido
from models.Usuario import Usuario
from db import db
import random
from sqlalchemy.exc import NoResultFound


class PedidoService:
    @staticmethod
    def find_all_pedidos_by_usuario_id(usuario_id, page, per_page):
        """
        Retorna todos os pedidos de um usuário com paginação.
        """
        pedidos_paginated = PedidoRepository.find_all_by_usuario_id(usuario_id, page, per_page)
        if not pedidos_paginated.items:
            raise Exception("Esse usuário não tem pedidos.")
        return pedidos_paginated

    @staticmethod
    def save_pedido(pedido):
        """
        Salva um pedido no banco de dados.
        """
        PedidoRepository.save(pedido)

    @staticmethod
    def create_pedido(data):
        """
        Cria um novo pedido associado a um usuário.
        """
        usuario = UsuarioRepository.find_by_id(data['usuario_id'])
        if not usuario:
            raise Exception("Usuário não encontrado.")

        pedido = Pedido(
            data_pedido=data['data_pedido'],
            valor_total=data['valor_total'],
            pedido_estado=data['pedido_estado'],
            usuario_id=usuario.usuario_id
        )
        PedidoService.save_pedido(pedido)
        return pedido

    @staticmethod
    def find_pedido_by_id(pedido_id):
        """
        Retorna um pedido específico pelo ID.
        """
        pedido = PedidoRepository.find_by_id(pedido_id)
        if not pedido:
            raise Exception("Nenhum pedido encontrado com esse ID.")
        return pedido

    # @staticmethod
    # def assign_produto_pedido(produtos, pedido_id, random_generator):
    #     """
    #     Associa produtos a um pedido gerando uma lista de ProdutoPedido.
    #     """
    #     produto_pedidos = []
    #     for produto in produtos:
    #         produto_pedido = ProdutoPedido(
    #             pedido_id=pedido_id,
    #             produto_id=produto.produto_id,
    #             quantidade=random_generator.randint(1, 5),
    #             preco_unitario=produto.preco,
    #             preco_total=produto.preco  # Exemplo simplificado
    #         )
    #         produto_pedidos.append(produto_pedido)
    #     return produto_pedidos
    #
    # @staticmethod
    # def create_many_pedidos(quantidade_pedidos, quantidade_produtos_diferentes, quantidade_usuarios):
    #     """
    #     Cria vários pedidos com produtos e associa aos usuários.
    #     """
    #     pedidos = []
    #     random_generator = random.Random()
    #
    #     produtos = ProdutoRepository.random_produtos(quantidade_produtos_diferentes)
    #     if not produtos:
    #         raise Exception("Nenhum produto encontrado.")
    #
    #     usuarios = UsuarioRepository.random_usuarios(quantidade_usuarios)
    #     if not usuarios:
    #         raise Exception("Nenhum usuário encontrado.")
    #
    #     for _ in range(quantidade_pedidos):
    #         usuario = random.choice(usuarios)
    #         produto_pedidos = PedidoService.assign_produto_pedido(produtos, None, random_generator)
    #
    #         pedido = Pedido(
    #             data_pedido=random_generator.choice(["2024-11-20", "2024-11-21"]),  # Exemplos de data
    #             valor_total=sum(pp.preco_total for pp in produto_pedidos),
    #             pedido_estado="PENDENTE",
    #             usuario_id=usuario.usuario_id
    #         )
    #         PedidoService.save_pedido(pedido)
    #
    #         for produto_pedido in produto_pedidos:
    #             produto_pedido.pedido_id = pedido.pedido_id
    #             ProdutoPedidoRepository.save(produto_pedido)
    #
    #         pedidos.append(pedido)
    #
    #     return pedidos
