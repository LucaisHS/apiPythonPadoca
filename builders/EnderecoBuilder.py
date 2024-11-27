import random
import uuid
from models.Endereco import Endereco


class EnderecoBuilder:
    def __init__(self):
        self.random = random.Random()

        self.cidades = [
            "Jundiaí", "Várzea Paulista", "Campo Limpo Paulista", "Itupeva", "Louveira",
            "Jarinu", "Vinhedo", "Cabreúva", "Itatiba", "Campinas", "Indaiatuba"
        ]

        self.ruas = [
            "Rua das Flores", "Avenida Paulista", "Rua do Comércio", "Rua das Acácias", "Avenida Central",
            "Rua dos Pinheiros", "Rua das Palmeiras", "Rua Santos Dumont", "Rua Rio Branco", "Rua Monte Alegre",
            "Rua Dom Pedro I", "Avenida Brasil", "Rua Visconde de Mauá", "Rua Sete de Setembro", "Rua São José",
            "Rua Tiradentes", "Rua da Liberdade", "Rua XV de Novembro", "Rua da Consolação", "Rua Bela Vista",
            "Avenida Getúlio Vargas", "Rua Marechal Deodoro", "Rua do Sol", "Rua das Oliveiras", "Rua das Orquídeas",
            "Rua dos Cravos", "Avenida Ipiranga", "Rua dos Lírios", "Rua dos Jacarandás", "Rua das Magnólias",
            "Rua Santa Clara", "Avenida Boa Vista", "Rua José Bonifácio", "Rua Independência", "Rua Gonçalves Dias",
            "Rua das Hortênsias", "Rua Presidente Kennedy", "Rua Santos", "Rua do Porto", "Rua Marechal Rondon",
            "Rua Castro Alves", "Rua das Laranjeiras", "Rua do Lago", "Rua das Camélias", "Rua Benjamin Constant",
            "Rua da Praia", "Rua São Paulo", "Avenida República", "Rua Duque de Caxias", "Rua Augusta",
            "Rua Professor Souza", "Rua das Andorinhas", "Avenida Rio Grande", "Rua dos Girassóis", "Rua dos Jasmins",
            "Rua das Margaridas", "Rua Santa Rita", "Rua do Progresso", "Rua Almeida Júnior", "Rua Dom Bosco",
            "Rua Francisco Xavier", "Rua Padre Cícero", "Rua Doutor Arnaldo", "Rua Barão do Rio Branco", "Rua da Saudade",
            "Rua Padre João", "Rua Adolfo Pinheiro", "Rua das Pedras", "Rua Carlos Gomes", "Rua Santa Teresa",
            "Rua Aurora", "Rua São Francisco", "Rua Miguel Couto", "Rua Maringá", "Rua Bento Gonçalves",
            "Avenida das Américas", "Rua das Graças", "Rua Santa Rosa", "Rua das Esmeraldas", "Rua Professor Fontes",
            "Rua Guilherme Marconi", "Rua Goiás", "Rua das Dores", "Rua Carlos Drummond", "Rua Pernambuco",
            "Rua das Rosas", "Rua das Amoras", "Rua Vicente de Carvalho", "Rua dos Bandeirantes", "Rua São Lucas",
            "Rua dos Guararapes", "Rua Oscar Freire", "Rua General Osório", "Rua Camargo", "Rua Pedro Álvares Cabral",
            "Avenida 9 de Julho", "Rua Ceará", "Rua das Bromélias", "Rua Quintino Bocaiúva", "Rua do Príncipe",
            "Rua das Figueiras", "Rua das Alamandas", "Rua Acre", "Rua Maestro Villa-Lobos", "Rua Marajó"
        ]

        self.bairros = [
            "Jardim das Flores", "Vila Nova", "Parque dos Sonhos", "Centro", "Vila Mariana",
            "Jardim Paulista", "Bela Vista", "Vila Esperança", "Parque Industrial", "Jardim América",
            "Vila Olímpia", "Jardim Europa", "Jardim São Paulo", "Vila Progresso", "Vila do Sol",
            "Vila Bela", "Vila Formosa", "Jardim Guanabara", "Parque dos Pássaros", "Vila Matilde",
            "Jardim das Acácias", "Vila Rica", "Bairro Alto", "Parque Verde", "Jardim Tropical",
            "Vila Rosa", "Vila União", "Bairro da Paz", "Jardim Esmeralda", "Vila Aurora",
            "Jardim Primavera", "Vila dos Anjos", "Vila Industrial", "Parque das Águas", "Jardim Santa Clara",
            "Vila São João", "Vila Esperança", "Bairro Novo", "Parque dos Lagos", "Jardim Eldorado"
        ]

        self.complementos = [
            "Apto 101", "Bloco B", "Casa 2", "Fundos", "Sobreloja", "Loja 3", "Térreo", "Cobertura", "Anexo", "Galpão",
            "Sala 205", "Edifício Alpha", "Prédio Comercial", "Quintal", "Subsolo", "Lote 12", "Barracão", "Andar 3",
            "Casa de Esquina", "Ponto de Referência: Próximo ao Supermercado"
        ]

    def choose_rua(self):
        return self.random.choice(self.ruas)

    def choose_bairro(self):
        return self.random.choice(self.bairros)

    def choose_cidade(self):
        return self.random.choice(self.cidades)

    def choose_complemento(self):
        return self.random.choice(self.complementos)

    def create_cep(self):
        return f"{''.join(str(self.random.randint(0, 9)) for _ in range(5))}-{''.join(str(self.random.randint(0, 9)) for _ in range(3))}"

    def create_num(self):
        return ''.join(str(self.random.randint(0, 9)) for _ in range(self.random.randint(1, 5)))

    def build_endereco(self, usuario_id=None):
        endereco = Endereco(
            rua=self.choose_rua(),
            numero=self.create_num(),
            bairro=self.choose_bairro(),
            cidade=self.choose_cidade(),
            CEP=self.create_cep(),
            complemento=self.choose_complemento(),
            usuario_id=usuario_id
        )
        return endereco
