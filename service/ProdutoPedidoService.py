from repositories.ProdutoPedidoRepository import ProdutoPedidoRepository
from models.ProdutoPedido import ProdutoPedido

class ProdutoPedidoService:
    @staticmethod
    def find_all_by_pedido_id(pedido_id):
        """
        Retorna todos os ProdutoPedido associados a um pedido específico.
        """
        produtos_pedido = ProdutoPedidoRepository.find_all_by_pedido_id(pedido_id)
        if not produtos_pedido:
            raise Exception("Esse pedido não possui nenhum item.")
        return produtos_pedido

    @staticmethod
    def save_produto_pedido(produto_pedido):
        """
        Salva um novo ProdutoPedido ou atualiza um existente.
        """
        ProdutoPedidoRepository.save(produto_pedido)

    @staticmethod
    def create_produto_pedido(data):
        """
        Cria um novo ProdutoPedido a partir dos dados fornecidos.
        """
        produto_pedido = ProdutoPedido(data)
        ProdutoPedidoService.save_produto_pedido(produto_pedido)
        return produto_pedido
