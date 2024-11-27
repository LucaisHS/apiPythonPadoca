from flask import Blueprint, jsonify, request
from service.EnderecoService import EnderecoService

endereco_bp = Blueprint('endereco_bp', __name__)

@endereco_bp.route('/enderecos', methods=['GET'])
def get_enderecos():
    enderecos = EnderecoService.get_enderecos()
    enderecos_list = [endereco.to_dict() for endereco in enderecos]
    return jsonify(enderecos_list), 200

@endereco_bp.route('/enderecos/<string:endereco_id>', methods=['GET'])
def get_endereco_by_id(endereco_id):
    endereco = EnderecoService.get_endereco_by_id(endereco_id)
    if endereco:
        return jsonify(endereco.to_dict()), 200
    return jsonify({'message': 'Endereço não encontrado'}), 404

@endereco_bp.route('/enderecos', methods=['POST'])
def create_endereco():
    data = request.get_json()
    endereco = EnderecoService.create_endereco(data)
    return jsonify(endereco.to_dict()), 201
