from datetime import datetime, timedelta
from typing import List

from repositories.UsuarioRepository import UsuarioRepository
from models import Usuario
from schemas.DateFormatterDTO import DateFormatterDTO


class UsuarioService:
    @staticmethod
    def create_usuario(data):
        usuario = Usuario(
            nome=data['nome'],
            sobrenome=data['sobrenome'],
            senha=data['senha'],
            telefone=data['telefone'],
            email=data['email']
        )
        UsuarioRepository.save(usuario)
        return usuario

    @staticmethod
    def get_usuarios():
        return UsuarioRepository.get_all()

    @staticmethod
    def get_usuario_by_id(usuario_id):
        return UsuarioRepository.find_by_id(usuario_id)

    def calc_idade_usuarios(idade: List[int]) -> DateFormatterDTO:
        hoje = datetime.now()

        if len(idade) != 2:
            raise ValueError("Cada array deve conter exatamente dois valores: [idade mínima, idade máxima]")

        # Garantir que idade[0] é a menor idade e idade[1] é a maior
        if idade[0] > idade[1]:
            idade[0], idade[1] = idade[1], idade[0]

        data_maxima = hoje - timedelta(days=idade[0] * 365.25)  # Calcula a data máxima
        data_minima = hoje - timedelta(days=idade[1] * 365.25)  # Calcula a data mínima

        # Obtém as datas de nascimento entre as faixas
        dates_list = UsuarioRepository.find_data_nascimento_between(data_minima, data_maxima)

        # Retorna o DTO com os resultados
        return DateFormatterDTO(idade[0], idade[1], len(dates_list))
