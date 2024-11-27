from flask import Blueprint, jsonify, request
from service.OpcoesService import OpcoesService
import uuid

opcoes_bp = Blueprint('opcoes_bp', __name__)

@opcoes_bp.route('/opcoes', methods=['POST'])
def add_opcao():
    """
    Adiciona uma nova opção.
    """
    data = request.get_json()
    try:
        opcao = OpcoesService.create_opcoes(data)
        return jsonify(opcao.to_dict()), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@opcoes_bp.route('/opcoes/<string:id>', methods=['GET'])
def get_all_opcoes_by_produto_id(id):
    """
    Retorna todas as opções de um produto específico.
    """
    try:
        opcoes = OpcoesService.find_opcao_by_produto_id(uuid.UUID(id).bytes)
        opcoes_list = [opcao.to_dict() for opcao in opcoes]
        return jsonify(opcoes_list), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@opcoes_bp.route('/opcoes/add/opcoes/<int:tipo>', methods=['POST'])
def add_many_opcoes(tipo):
    """
    Adiciona várias opções para produtos.
    """
    data = request.get_json()
    try:
        opcoes = OpcoesService.create_many_opcoes(data, tipo)
        opcoes_list = [opcao.to_dict() for opcao in opcoes]
        return jsonify(opcoes_list), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400
