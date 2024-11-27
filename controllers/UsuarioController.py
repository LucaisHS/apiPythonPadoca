import time
import tracemalloc

from flask import Blueprint, jsonify, request
from service.UsuarioService import UsuarioService

# Cria um blueprint para separar as rotas de usuario
usuario_bp = Blueprint('usuario_bp', __name__)

@usuario_bp.route('/usuario', methods=['GET'])
def get_usuarios():
    usuarios = UsuarioService.get_usuarios()
    usuarios_list = [usuario.to_dict() for usuario in usuarios]
    return jsonify(usuarios_list), 200

@usuario_bp.route('/usuario', methods=['POST'])
def create_usuario():
    data = request.get_json()
    usuario = UsuarioService.create_usuario(data)
    return jsonify(usuario.to_dict()), 201

import time
import tracemalloc
from flask import Blueprint, jsonify, request
from service.UsuarioService import UsuarioService

usuario_bp = Blueprint("usuario_bp", __name__)

@usuario_bp.route('/usuario/graf/idades', methods=['GET'])
def data_graph_old():
    try:
        # Inicia a medição de tempo e memória
        start_time = time.time()
        tracemalloc.start()

        # Processamento da API
        min_ages = request.args.getlist('minAges', type=int)
        max_ages = request.args.getlist('maxAges', type=int)

        if len(min_ages) != len(max_ages):
            return jsonify({'message': 'O número de idades mínimas deve ser igual ao número de idades máximas.'}), 400

        data = []
        for i in range(len(min_ages)):
            args = [min_ages[i], max_ages[i]]
            result = UsuarioService.calc_idade_usuarios(args)
            data.append(result.to_dict())  # Converte para dicionário

        # Finaliza a medição de tempo e memória
        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Adiciona os metadados de tempo e memória
        response = {
            'data': data,
            'meta': {
                'tempo': f"{end_time - start_time:.4f} seconds",
                'memoria_usada': f"{current / 1024:.2f} KB",
                'pico_memoria': f"{peak / 1024:.2f} KB"
            }
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'message': str(e)}), 500



