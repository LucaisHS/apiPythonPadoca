import time
from datetime import datetime

import psutil
from flask import Blueprint, jsonify, request

from service.OpcoesService import OpcoesService
from service.PedidoService import PedidoService
# from service.ProdutoPedidoService import ProdutoPedidoService
# from service.OpcoesService import OpcoesService
# from service.ProdutoService import ProdutoService
from models.Pedido import Pedido
# from models.ProdutoPedido import ProdutoPedido
import uuid

from service.ProdutoPedidoService import ProdutoPedidoService
from service.ProdutoService import ProdutoService

pedido_bp = Blueprint('pedido_bp', __name__)

@pedido_bp.route('/pedido', methods=['POST'])
def add_pedido():
    """
    Adiciona um novo pedido.
    """
    data = request.get_json()
    try:
        pedido = PedidoService.create_pedido(data)
        return jsonify(pedido.to_dict()), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@pedido_bp.route('/pedido/<string:usuario_id>', methods=['GET'])
def get_all_pedidos_by_usuario_id(usuario_id):
    """
    Retorna todos os pedidos de um usuário com paginação.
    """
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('size', default=10, type=int)
    try:
        # Converte o UUID para binário
        usuario_id_bin = uuid.UUID(usuario_id).bytes

        # Obtém os pedidos paginados
        pedidos_paginated = PedidoService.find_all_pedidos_by_usuario_id(usuario_id_bin, page, per_page)

        # Serializa os pedidos
        pedidos_list = [pedido.to_dict() for pedido in pedidos_paginated.items]
        return jsonify({
            'pedidos': pedidos_list,
            'total': pedidos_paginated.total,
            'page': pedidos_paginated.page,
            'pages': pedidos_paginated.pages
        }), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@pedido_bp.route('/pedido/produtos/<string:pedido_id>', methods=['GET'])
def get_all_products_by_order_id(pedido_id):
    """
    Retorna todos os produtos associados a um pedido.
    """
    try:
        produtos_pedido = ProdutoPedidoService.find_all_by_pedido_id(uuid.UUID(pedido_id).bytes)
        produtos_list = [pp.to_dict() for pp in produtos_pedido]
        return jsonify(produtos_list), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@pedido_bp.route('/pedido/produtos/add', methods=['POST'])
def add_item_on_pedido():
    """
    Adiciona um produto a um pedido.
    """
    data = request.get_json()
    try:
        pp = ProdutoPedidoService.create_produto_pedido(data)
        opcao = OpcoesService.find_opcao_by_id(data['opcao_id'])
        produto = ProdutoService.find_produto_by_id(data['produto_id'])
        pedido = PedidoService.find_pedido_by_id(data['pedido_id'])
        pp.opcao = opcao
        pp.produto = produto
        pp.pedido = pedido
        ProdutoPedidoService.save(pp)
        return jsonify(pp.to_dict()), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400


# @pedido_bp.route('/pedido/add/pedidos/<int:quantidade_pedido>/<int:quantidade_produto>/<int:quantidade_usuarios>', methods=['POST'])
# def create_many_pedidos(quantidade_pedido, quantidade_produto, quantidade_usuarios):
#     """
#     Cria múltiplos pedidos com produtos e usuários associados.
#     """
#     try:
#         pedidos = PedidoService.create_many_pedidos(quantidade_pedido, quantidade_produto, quantidade_usuarios)
#         pedidos_list = [pedido.to_dict() for pedido in pedidos]
#         return jsonify(pedidos_list), 201
#     except Exception as e:
#         return jsonify({'message': str(e)}), 400

@pedido_bp.route("/pedido/novos/pedidos/dias", methods=["GET"])
def new_pedidos_in_x_days():
    try:
        dias = int(request.args.get("dias", 7))

        start_time = time.perf_counter()
        process = psutil.Process()
        memory_before = process.memory_info().rss

        quantidade = PedidoService.get_quantidade_pedido(dias)

        end_time = time.perf_counter()
        memory_after = process.memory_info().rss

        time_elapsed = (end_time - start_time) * 1000  # ms
        memory_used = (memory_after - memory_before) / 1024  # KB

        return jsonify({
            "quantidade": quantidade,
            "tempo_usado": f"{time_elapsed:.4f} ms",
            "memoria_usada": f"{memory_used:.2f} KB"
        }), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@pedido_bp.route("/pedido/count", methods=["GET"])
def count_pedidos():
    try:
        start_time = time.perf_counter()
        process = psutil.Process()
        memory_before = process.memory_info().rss

        quantidade = PedidoService.count_pedidos()

        end_time = time.perf_counter()
        memory_after = process.memory_info().rss

        time_elapsed = (end_time - start_time) * 1000  # ms
        memory_used = (memory_after - memory_before) / 1024  # KB

        return jsonify({
            "quantidade_pedidos": quantidade,
            "meta": {
                "tempo": f"{time_elapsed:.4f} ms",
                "memoria_usada": f"{memory_used:.2f} KB"
            }

        }), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@pedido_bp.route("/pedido/mediaQuantidade", methods=["GET"])
def get_media_pedidos_por_usuario():
    try:
        start_time = time.perf_counter()
        process = psutil.Process()
        memory_before = process.memory_info().rss

        media = float(PedidoService.find_avg_pedidos_por_usuario())

        end_time = time.perf_counter()
        memory_after = process.memory_info().rss

        time_elapsed = (end_time - start_time) * 1000  # ms
        memory_used = (memory_after - memory_before) / 1024  # KB

        return jsonify({
            "quantidade": media,
            "meta": {
                "tempo": f"{time_elapsed:.4f} ms",
                "memoria_usada": f"{memory_used:.2f} KB"
            }
        }), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@pedido_bp.route("/pedido/contagem/formas-pagamento", methods=["GET"])
def get_contagem_por_forma_pagamento():
    try:
        start_time = time.perf_counter()
        process = psutil.Process()
        memory_before = process.memory_info().rss

        formas_pagamento = PedidoService.contar_pedidos_por_forma_pagamento()

        end_time = time.perf_counter()
        memory_after = process.memory_info().rss

        time_elapsed = (end_time - start_time) * 1000  # ms
        memory_used = (memory_after - memory_before) / 1024  # KB

        return jsonify({
            "Metodos de pagamento:": formas_pagamento,
            "meta": {
                "tempo": f"{time_elapsed:.4f} ms",
                "memoria_usada": f"{memory_used:.2f} KB"
            }
        }), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@pedido_bp.route("/pedido/horariosVendas", methods=["GET"])
def get_horarios_por_intervalo():
    try:
        data = request.args.get("data")
        # Converte a data para o formato esperado pelo banco (YYYY-MM-DD)
        data_formatada = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")

        start_time = time.perf_counter()
        process = psutil.Process()
        memory_before = process.memory_info().rss

        horarios = PedidoService.contar_horarios_por_intervalo(data_formatada)

        end_time = time.perf_counter()
        memory_after = process.memory_info().rss

        time_elapsed = (end_time - start_time) * 1000  # ms
        memory_used = (memory_after - memory_before) / 1024  # KB

        return jsonify({
            "horarios": horarios,
            "tempo_usado": f"{time_elapsed:.4f} ms",
            "memoria_usada": f"{memory_used:.2f} KB"
        }), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@pedido_bp.route("/pedido/horariosPicoGlobal", methods=["GET"])
def get_horarios_por_intervalo_global():
    """
    Retorna os horários de pico global (considerando todos os horários de pedidos).
    """
    try:
        # Início da medição de tempo e memória
        start_time = time.perf_counter()
        process = psutil.Process()
        memory_before = process.memory_info().rss

        # Chama o serviço para contar os horários
        data_result = PedidoService.contar_horarios_por_intervalo_global()

        # Fim da medição de tempo e memória
        end_time = time.perf_counter()
        memory_after = process.memory_info().rss

        # Calcula métricas
        time_elapsed = (end_time - start_time) * 1000  # Tempo em ms
        memory_used = (memory_after - memory_before) / 1024  # Memória em KB

        # Constrói a resposta
        response = {
            "horarios_pico_global": data_result,
            "meta": {
                "tempo": f"{time_elapsed:.4f} ms",
                "memoria_usada": f"{memory_used:.2f} KB"
            }
        }

        return jsonify(response), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@pedido_bp.route('/pedido/valoresIntervalos', methods=['GET'])
def get_pedidos_por_intervalo_de_valores():
    """
    Retorna a contagem de pedidos por intervalo de valores.
    """
    try:
        # Início da medição de tempo e memória
        start_time = time.perf_counter()
        process = psutil.Process()
        memory_before = process.memory_info().rss

        # Obtém os dados do serviço
        data = PedidoService.contar_pedidos_por_intervalo_de_valores()

        # Fim da medição de tempo e memória
        end_time = time.perf_counter()
        memory_after = process.memory_info().rss

        # Calcula métricas
        time_elapsed = (end_time - start_time) * 1000  # Tempo em ms
        memory_used = (memory_after - memory_before) / 1024  # Memória em KB

        # Cria a resposta com os dados e as métricas
        response = {
            "dados": data,
            "meta": {
                "tempo": f"{time_elapsed:.4f} ms",
                "memoria_usada": f"{memory_used:.2f} KB"
            }
        }

        return jsonify(response), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500




@pedido_bp.route("/pedido/valorMedio", methods=["GET"])
def get_valor_medio_pedidos():
    try:
        start_time = time.perf_counter()
        process = psutil.Process()
        memory_before = process.memory_info().rss

        valor_medio = float(PedidoService.calcular_valor_medio_pedidos())

        end_time = time.perf_counter()
        memory_after = process.memory_info().rss

        time_elapsed = (end_time - start_time) * 1000  # ms
        memory_used = (memory_after - memory_before) / 1024  # KB

        return jsonify({
            "valor_medio": valor_medio,
            "tempo_usado": f"{time_elapsed:.4f} ms",
            "memoria_usada": f"{memory_used:.2f} KB"
        }), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@pedido_bp.route("/pedido/maiorValor", methods=["GET"])
def get_pedido_de_maior_valor():
    try:
        start_time = time.perf_counter()
        process = psutil.Process()
        memory_before = process.memory_info().rss

        pedido = PedidoService.buscar_pedido_de_maior_valor()

        end_time = time.perf_counter()
        memory_after = process.memory_info().rss

        time_elapsed = (end_time - start_time) * 1000  # ms
        memory_used = (memory_after - memory_before) / 1024  # KB

        return jsonify({
            "pedido_maior_valor": pedido.to_dict(),
            "tempo_usado": f"{time_elapsed:.4f} ms",
            "memoria_usada": f"{memory_used:.2f} KB"

        }), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@pedido_bp.route('/pedido/all', methods=['GET'])
def get_all_pedidos():
    """
    Retorna todos os pedidos com paginação.
    """
    try:
        # Obtém os parâmetros de paginação da requisição
        page = int(request.args.get('page', 1))  # Página atual (padrão: 1)
        per_page = int(request.args.get('size', 10))  # Número de itens por página (padrão: 10)

        # Busca os pedidos com paginação no serviço
        pedidos_paginated = PedidoService.get_all_pedidos(page, per_page)

        # Serializa os dados e adiciona informações de paginação
        response = {
            "pedidos": [pedido.to_dict() for pedido in pedidos_paginated.items],
            "pagina_atual": pedidos_paginated.page,
            "total_paginas": pedidos_paginated.pages,
            "total_itens": pedidos_paginated.total,
        }

        return jsonify(response), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

