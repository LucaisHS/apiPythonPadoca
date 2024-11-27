from random import randint

from repositories.OpcoesRepository import OpcoesRepository
from repositories.ProdutoRepository import ProdutoRepository
from models.Opcoes import Opcoes

class OpcoesService:
    @staticmethod
    def find_opcao_by_produto_id(produto_id):
        """
        Retorna todas as opções de um produto específico.
        """
        produto = ProdutoRepository.find_produto_by_produto_id(produto_id)
        if not produto:
            raise Exception("Produto não encontrado!")
        return produto.opcoes

    @staticmethod
    def find_opcao_by_id(opcao_id):
        """
        Retorna uma opção pelo ID.
        """
        opcao = OpcoesRepository.find_opcoes_by_opcao_id(opcao_id)
        if not opcao:
            raise Exception("Opção não encontrada!")
        return opcao

    @staticmethod
    def save_opcao(opcao):
        """
        Salva ou atualiza uma opção.
        """
        OpcoesRepository.save(opcao)

    @staticmethod
    def create_opcoes(data):
        """
        Cria uma nova opção e a associa a um produto existente.
        """
        opcao = Opcoes(
            nome=data['nome'],
            preco_add=data['preco_add']
        )
        produto = ProdutoRepository.find_produto_by_produto_id(data['produto_id'])
        if not produto:
            raise Exception("Nenhum produto com esse ID foi encontrado")

        opcao.produtos.append(produto)
        produto.opcoes.append(opcao)
        OpcoesService.save_opcao(opcao)
        return opcao

    @staticmethod
    def create_many_opcoes(produtos, tipo):
        """
        Cria múltiplas opções para uma lista de produtos.
        """
        opcoes = []
        for produto in produtos:
            for i in range(3):  # Substituir 3 pelo número de opções desejadas
                opcao = Opcoes(
                    nome=f"Opção {tipo}-{i}",
                    preco_add=randint(1, 10)
                )
                opcao.produtos.append(produto)
                produto.opcoes.append(opcao)
                OpcoesService.save_opcao(opcao)
                opcoes.append(opcao)
        return opcoes
