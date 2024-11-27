from flask import Blueprint, jsonify, request
from service.ProdutoService import ProdutoService
import uuid

produto_bp = Blueprint('produto_bp', __name__)

@produto_bp.route('/produto', methods=['POST'])
def add_produto():
    """
    Adiciona um novo produto.
    """
    data = request.get_json()
    try:
        produto = ProdutoService.create_produto(data)
        return jsonify(produto.to_dict()), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@produto_bp.route('/produto', methods=['GET'])
def get_all_produtos():
    """
    Retorna todos os produtos com paginação.
    """
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('size', default=10, type=int)
    try:
        produtos_paginated = ProdutoService.find_all_produtos(page, per_page)
        produtos_list = [produto.to_dict() for produto in produtos_paginated.items]
        return jsonify({
            'produtos': produtos_list,
            'total': produtos_paginated.total,
            'page': produtos_paginated.page,
            'pages': produtos_paginated.pages
        }), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@produto_bp.route('/produto/<string:id>', methods=['GET'])
def get_produto_by_id(id):
    """
    Retorna um produto pelo ID.
    """
    try:
        produto = ProdutoService.find_produto_by_id(uuid.UUID(id).bytes)
        return jsonify(produto.to_dict()), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@produto_bp.route('/produto/add/produtos/<int:max_estoque>', methods=['POST'])
def add_many_produtos(max_estoque):
    """
    Adiciona vários produtos com estoque gerado automaticamente.
    """
    try:
        produtos = ProdutoService.create_many_produtos(max_estoque)
        produtos_list = [produto.to_dict() for produto in produtos]
        return jsonify(produtos_list), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400
