import random
import string
from datetime import date, timedelta
from models.Usuario import Usuario


class UsuarioBuilder:
    def __init__(self):
        self.random = random.Random()
        self.names = [
            "Lucas", "Maria", "João", "Ana", "Pedro", "Carla", "Marcos", "Fernanda", "Roberto", "Julia",
            "Gabriel", "Sofia", "Paulo", "Larissa", "Ricardo", "Beatriz", "Daniel", "Tatiana", "Felipe", "Mariana",
            "Gustavo", "Camila", "Thiago", "Aline", "Leandro", "Patricia", "Cesar", "Vanessa", "Rodrigo", "Elisa",
            "Igor", "Renata", "Rafael", "Clara", "Vinicius", "Amanda", "André", "Diana", "Fernando", "Isabela",
            "Vitor", "Alice", "Carlos", "Helena", "Otavio", "Bruna", "Diego", "Luana", "Antonio", "Valeria",
            "Henrique", "Simone", "Murilo", "Cristina", "Bruno", "Juliana", "Samuel", "Leticia", "Edson", "Raquel",
            "Jose", "Monica", "Victor", "Bianca", "Mateus", "Melissa", "Ivan", "Gabriela", "Eduardo", "Lorena",
            "Leonardo", "Luisa", "Alexandre", "Isadora", "Miguel", "Paula", "Sergio", "Caroline", "Julio", "Barbara",
            "Caio", "Regina", "Artur", "Flavia", "Fábio", "Renata", "Ronaldo", "Geovana", "Marcelo", "Talita",
            "Jorge", "Daniela", "Luis", "Natalia", "Alessandro", "Sabrina", "Elias", "Vanessa", "Rui", "Isabel"
        ]
        self.emails = ["gmail", "hotmail", "yahoo", "outlook", "icloud"]
        self.CHARACTERS = string.ascii_letters + string.digits + "!@#$%_-"

    def make_names_and_email(self):
        index1 = self.random.randint(0, len(self.names) - 1)
        index2 = self.random.randint(0, len(self.names) - 1)

        while index1 == index2:
            index2 = self.random.randint(0, len(self.names) - 1)

        email = f"{self.names[index1]}{self.names[index2]}@{self.random.choice(self.emails)}.com"
        return self.names[index1], self.names[index2], email

    def make_password(self, length=8):
        return ''.join(self.random.choices(self.CHARACTERS, k=length))

    def make_telefone(self):
        telefone = f"11 9{''.join(str(self.random.randint(0, 9)) for _ in range(4))}-{''.join(str(self.random.randint(0, 9)) for _ in range(4))}"
        return telefone

    def make_data_nascimento(self, start_year=1943, end_year=2006):
        start_date = date(start_year, 1, 1)
        end_date = date(end_year, 12, 31)
        delta = end_date - start_date
        random_days = self.random.randint(0, delta.days)
        return start_date + timedelta(days=random_days)

    def build_usuario(self):
        first_name, last_name, email = self.make_names_and_email()
        password = self.make_password()
        telefone = self.make_telefone()
        nascimento = self.make_data_nascimento()

        usuario = Usuario(
            nome=first_name,
            sobrenome=last_name,
            senha=password,
            telefone=telefone,
            email=email,
            data_nascimento=nascimento
        )
        return usuario
