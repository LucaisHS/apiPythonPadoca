import time
import tracemalloc
from datetime import datetime, timedelta

import psutil
from flask import Blueprint, jsonify, request
from service.UsuarioService import UsuarioService


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

@usuario_bp.route('/usuario/graf/idades', methods=['GET'])
def data_graph_old():
    try:

        start_time = time.time()
        tracemalloc.start()


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
@usuario_bp.route('/usuario/add/usuarios/<int:qntd>', methods=['POST'])
def add_many_usuarios(qntd):
    try:

        start_time = time.time()
        tracemalloc.start()

        novos_usuarios = UsuarioService.createManyUsuarios(qntd)

        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        response = {
            'data': [usuario.to_dict() for usuario in novos_usuarios],
            'meta': {
                'tempo': f"{end_time - start_time:.4f} segundos",
                'memoria_usada': f"{current / 1024:.2f} KB",
                'pico_memoria': f"{peak / 1024:.2f} KB"
            }
        }
        return jsonify(response), 201

    except Exception as e:
        return jsonify({'message': str(e)}), 500


@usuario_bp.route('/usuario/novos/usuarios/dias', methods=['GET'])
def new_usuarios_in_x_days():

    try:
        dias = int(request.args.get('dias', 7))

        start_time = time.perf_counter()
        process = psutil.Process()
        memory_before = process.memory_info().rss

        quantidade = UsuarioService.get_new_users_between(dias)

        end_time = time.perf_counter()
        memory_after = process.memory_info().rss

        time_elapsed = (end_time - start_time) * 1000  # Tempo em ms
        memory_used = (memory_after - memory_before) / 1024  # Memória usada em KB

        response = {
            "quantidade": quantidade,
            "tempo_usado": f"{time_elapsed:.4f} ms",
            "memoria_usada": f"{memory_used:.2f} KB"
        }

        return jsonify(response), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

