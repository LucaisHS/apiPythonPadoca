from decimal import Decimal
from models.Opcoes import Opcoes
from models.Produto import Produto


class OpcaoBuilder:
    def __init__(self):
        self.opcoes_produtos = [
            "Tradicional", "Integral", "Pequeno", "Grande", "Com Cobertura", "Sem Cobertura",
            "Multigrãos", "Sem Grãos", "Simples", "Recheado", "Recheado com Creme", "Recheado com Doce de Leite",
            "Carne", "Frango", "Salgado", "Doce", "Especial", "Com Bacon"
        ]

        self.tamanhos_bebidas = ["Pequeno", "Grande"]

        self.precos_produtos = [
            Decimal("0.50"), Decimal("0.75"), Decimal("0.20"), Decimal("0.40"), Decimal("1.00"),
            Decimal("0.50"), Decimal("0.30"), Decimal("0.00"), Decimal("0.00"), Decimal("1.50"),
            Decimal("0.50"), Decimal("0.70"), Decimal("0.00"), Decimal("0.30"), Decimal("0.00"),
            Decimal("0.20"), Decimal("0.00"), Decimal("0.60")
        ]

        self.precos_bebidas = [
            Decimal("0.00"), Decimal("1.00"), Decimal("0.00"), Decimal("1.50")
        ]

    def _select_names(self, tipo, index):
        """
        Seleciona os nomes das opções baseadas no tipo.
        """
        if tipo == "PRODUTO":
            start = index * 2
            return [self.opcoes_produtos[start], self.opcoes_produtos[start + 1]]
        elif tipo == "BEBIDA":
            return self.tamanhos_bebidas

    def _select_prices(self, tipo, index):
        """
        Seleciona os preços adicionais das opções baseadas no tipo.
        """
        if tipo == "PRODUTO":
            start = index * 2
            return [self.precos_produtos[start], self.precos_produtos[start + 1]]
        elif tipo == "BEBIDA":
            return self.precos_bebidas

    def build_opcoes(self, tipo, index, produtos=None):
        """
        Constrói uma lista de opções para um tipo e índice fornecidos.
        """
        nomes = self._select_names(tipo, index)
        precos = self._select_prices(tipo, index)

        opcoes = []
        for i in range(len(nomes)):
            produto_id = produtos[i].produto_id if produtos else None
            opcao = Opcoes(
                nome=nomes[i],
                preco_add=precos[i],
                produtos=[Produto(produto_id=produto_id)] if produto_id else []
            )
            opcoes.append(opcao)
        return opcoes
