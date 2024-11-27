from repositories.EnderecoRepository import EnderecoRepository
from models.Endereco import Endereco

class EnderecoService:
    @staticmethod
    def create_endereco(data):
        """
        Cria um novo endereço com base nos dados fornecidos.
        """
        endereco = Endereco(
            rua=data['rua'],
            numero=data['numero'],
            bairro=data['bairro'],
            cidade=data['cidade'],
            cep=data['cep'],
            complemento=data.get('complemento'),  # 'complemento' é opcional
            usuario_id=data['usuario_id']  # Associa o endereço ao usuário
        )
        EnderecoRepository.save(endereco)
        return endereco

    @staticmethod
    def get_enderecos():
        """
        Retorna todos os endereços.
        """
        return EnderecoRepository.get_all()

    @staticmethod
    def get_endereco_by_id(endereco_id):
        """
        Retorna um endereço específico pelo seu ID.
        """
        return EnderecoRepository.find_by_id(endereco_id)

    @staticmethod
    def get_enderecos_by_usuario_id(usuario_id):
        """
        Retorna todos os endereços associados a um usuário específico.
        """
        return EnderecoRepository.find_by_usuario_id(usuario_id)
