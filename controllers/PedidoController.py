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
