from datetime import datetime, timedelta, time

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

    from datetime import datetime, timedelta, time
    from repositories.PedidoRepository import PedidoRepository


    @staticmethod
    def get_quantidade_pedido(dias):
        today = datetime.now().date()
        start_date = today - timedelta(days=dias)
        return PedidoRepository.count_pedido_by_data_pedido_between(start_date, today)

    @staticmethod
    def count_pedidos():
        return PedidoRepository.count()

    @staticmethod
    def find_avg_pedidos_por_usuario():
        return PedidoRepository.find_average_pedidos_per_usuario()

    @staticmethod
    def contar_pedidos_por_forma_pagamento():
        resultados = PedidoRepository.count_pedidos_by_forma_pagamento()

        def process_row(row):
            forma_pagamento = row[0].value if row[0] is not None else None
            return {
                "formaPagamento": forma_pagamento,
                "quantidade": row[1] if row[1] is not None else 0
            }

        return [process_row(row) for row in resultados]

    @staticmethod
    def contar_horarios_por_intervalo(data):
        horarios = PedidoRepository.find_horarios_by_data(data)
        contagem_por_hora = {}

        for horario in horarios:
            # Verifica se o tipo é timedelta e converte para time
            if isinstance(horario, timedelta):  # Corrige o uso de timedelta
                total_seconds = int(horario.total_seconds())
                horas = total_seconds // 3600
                minutos = (total_seconds % 3600) // 60
                horario = time(horas, minutos)

            # Arredonda para o início da hora (desconsidera minutos e segundos)
            hora_inicio = horario.replace(minute=0, second=0, microsecond=0)
            contagem_por_hora[hora_inicio] = contagem_por_hora.get(hora_inicio, 0) + 1

        # Retorna o resultado no formato desejado
        return [{"hora": hora.strftime("%H:%M"), "quantidade": quantidade} for hora, quantidade in
                contagem_por_hora.items()]

    @staticmethod
    def contar_horarios_por_intervalo_global():
        horarios = PedidoRepository.find_all_horarios()
        contagem_por_hora = {}

        for horario in horarios:
            # Verifica se o tipo é timedelta e converte para time
            if isinstance(horario, timedelta):  # Corrige o uso de timedelta
                total_seconds = int(horario.total_seconds())
                horas = total_seconds // 3600
                minutos = (total_seconds % 3600) // 60
                horario = time(horas, minutos)

            # Arredonda para o início da hora (desconsidera minutos e segundos)
            hora_inicio = horario.replace(minute=0, second=0, microsecond=0)
            contagem_por_hora[hora_inicio] = contagem_por_hora.get(hora_inicio, 0) + 1

        # Retorna o resultado no formato desejado
        return [{"hora": hora.strftime("%H:%M"), "quantidade": quantidade} for hora, quantidade in
                contagem_por_hora.items()]

    @staticmethod
    def contar_pedidos_por_intervalo_de_valores():
        """
        Conta os pedidos por intervalo de valores e retorna uma lista formatada.
        """
        resultados = PedidoRepository.count_pedidos_por_intervalo_de_valores()

        intervalo_formatado = []
        for resultado in resultados:
            intervalo = resultado[0]  # O intervalo retornado do banco, como "0-50" ou ">251"
            quantidade = int(resultado[1])  # Quantidade de pedidos no intervalo

            # Converte o intervalo para uma lista de inteiros
            if intervalo == ">251":
                range_intervalo = [251]  # Apenas um elemento para ">251"
            else:
                limites = intervalo.split("-")  # Divide o intervalo em limites
                range_intervalo = [int(limites[0]), int(limites[1])]  # Converte limites para inteiros

            intervalo_formatado.append({
                "intervalo": range_intervalo,
                "quantidade": quantidade
            })

        return intervalo_formatado

    @staticmethod
    def calcular_valor_medio_pedidos():
        valor_medio = PedidoRepository.calcular_valor_medio_pedidos()
        return valor_medio if valor_medio is not None else 0

    @staticmethod
    def buscar_pedido_de_maior_valor():
        return PedidoRepository.buscar_pedido_de_maior_valor()

    @staticmethod
    def get_all_pedidos(page, per_page):
        return PedidoRepository.find_all_paginated(page, per_page)

