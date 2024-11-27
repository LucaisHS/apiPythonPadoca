from repositories.ProdutoRepository import ProdutoRepository
from models.Produto import Produto
from uuid import UUID
from random import randint

class ProdutoService:
    @staticmethod
    def find_all_produtos(page, per_page):
        """
        Retorna todos os produtos com paginação.
        """
        return ProdutoRepository.find_all(page, per_page)

    @staticmethod
    def find_produto_by_id(produto_id):
        """
        Retorna um produto pelo ID.
        """
        produto = ProdutoRepository.find_produto_by_produto_id(produto_id)
        if not produto:
            raise Exception("Produto não encontrado!")
        return produto

    @staticmethod
    def save_produto(produto):
        """
        Salva ou atualiza um produto.
        """
        ProdutoRepository.save(produto)

    @staticmethod
    def create_produto(data):
        """
        Cria um novo produto a partir dos dados fornecidos.
        """
        produto = Produto(**data)
        ProdutoService.save_produto(produto)
        return produto

    @staticmethod
    def create_many_produtos(max_estoque):
        """
        Cria múltiplos produtos com dados gerados automaticamente.
        """
        produtos = []
        for i in range(10):  # Substituir 10 pelo número desejado de produtos
            produto = Produto(
                nome=f"Produto {i}",
                descricao=f"Descrição do Produto {i}",
                preco=randint(10, 100),
                estoque=randint(1, max_estoque),
                categoria="Categoria Teste",
                imagem_url=f"http://example.com/produto_{i}.jpg"
            )
            ProdutoRepository.save(produto)
            produtos.append(produto)
        return produtos

    @staticmethod
    def random_produtos(quantidade):
        """
        Retorna uma lista de produtos aleatórios.
        """
        if quantidade <= 0:
            raise Exception("Digite um valor maior que 0")
        produto_ids = ProdutoRepository.find_all_ids()
        produtos_selecionados = [ProdutoRepository.find_produto_by_produto_id(id) for id in produto_ids[:quantidade]]
        return produtos_selecionados
