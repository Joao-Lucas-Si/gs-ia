from enum import Enum
import random
from typing import Tuple
from pydantic import BaseModel



class EstadoBrasileiro(Enum):
    SAO_PAULO = "São Paulo"
    AMAZONAS = "Amazonas"
    PARA = "Pará"
    MATO_GROSSO = "Mato grosso"
    PORAIMA = "Roraima"
    AMAPA = "Amapá"
    ACRE = "Acre"
    RONDONIA = "Rondônia"
    MATO_GROSSO_DO_SUL = "Mato Grosso do Sul"
    RIO_JANEIRO = "Rio de Janeiro"
    ESPIRITO_SANTO = "Espírito Santo"
    GOIAS = "Goiás"
    PARANA = "Paraná"
    TOCANTIS = "Tocantis"
    MARANHAO = "Maranhão"
    PARAIBA = "Paraíba"
    PERNAMBUCO = "Pernambuco"
    MINAS_GERAIS = "Minas Gerais"
    ALAGOAS = "Alagoas"
    SERGIPE = "Sergipe"
    BAHIA = "Bahia"
    CEARA = "Ceará"
    PIAUI = "Piauí"
    RORAIMA = "Roraima"
    RIO_GRANDE_NORTE = "Rio grande do Norte"
    SANTA_CATARINA = "Santa Catarina"
    RIO_GRANDE_SUL = "Rio Grande do Sul"


class Estado(Enum):
    CRITICO = "crítico"
    ATENCAO="atenção"
    ESTAVEL="estavel"


class Tendencia(BaseModel):
    intervalo: Tuple[int, int]
    estado_alvo: Estado = Estado.ESTAVEL

    def afetar(self, valor: int):
        area = self.intervalo[1] - self.intervalo[0]
        minimo = int(area * 0.05)
        maximo = int(area * 0.1)
        if not ((self.intervalo[0] + minimo) < valor < (self.intervalo[1] - minimo)):
            if valor < self.intervalo[0] + minimo:
                return valor + random.randint(minimo, maximo)
            else:
                return valor - random.randint(minimo, maximo)
        else:
            maior_menor = random.randint(0, 1)

            if maior_menor == 1:
                return valor + random.randint(minimo, maximo)
            else:
                return valor - random.randint(minimo, maximo)


class Tendencias(Enum):
    ENERGIA_CRITICA = Tendencia(intervalo=(0, 30), estado_alvo=Estado.CRITICO)
    ENERGIA_ATENCAO = Tendencia(intervalo=(30, 60), estado_alvo=Estado.ATENCAO)
    ENERGIA_ESTAVEL = Tendencia(intervalo=(60, 100), estado_alvo=Estado.ESTAVEL)
    TEMPERATURA_CRITICA = Tendencia(intervalo=(60, 100), estado_alvo=Estado.CRITICO)
    TEMPERATURA_ATENCAO = Tendencia(intervalo=(30, 60), estado_alvo=Estado.ATENCAO)
    TEMPERATURA_ESTAVEL = Tendencia(intervalo=(0, 30), estado_alvo=Estado.ESTAVEL)
    COMUNICACAO_CRITICA = Tendencia(intervalo=(0, 50), estado_alvo=Estado.CRITICO)
    COMUNICACAO_ATENCAO = Tendencia(intervalo=(50, 70), estado_alvo=Estado.ATENCAO)
    COMUNICACAO_ESTAVEL = Tendencia(intervalo=(70, 100), estado_alvo=Estado.ESTAVEL)
    LATENCIA_CRITICA = Tendencia(intervalo=(150, 200), estado_alvo=Estado.CRITICO)
    LATENCIA_ATENCAO = Tendencia(intervalo=(80, 150), estado_alvo=Estado.ATENCAO)
    LATENCIA_ESTAVEL = Tendencia(intervalo=(10, 80), estado_alvo=Estado.ESTAVEL)
    THROUGHPUT_CRITICA = Tendencia(intervalo=(0, 50), estado_alvo=Estado.CRITICO)
    THROUGHPUT_ATENCAO = Tendencia(intervalo=(50, 100), estado_alvo=Estado.ATENCAO)
    THROUGHPUT_ESTAVEL = Tendencia(intervalo=(100, 200), estado_alvo=Estado.ESTAVEL)
    SAUDE_ANTENA_CRITICA = Tendencia(intervalo=(0, 50), estado_alvo=Estado.CRITICO)
    SAUDE_ANTENA_ATENCAO = Tendencia(intervalo=(50, 70), estado_alvo=Estado.ATENCAO)
    SAUDE_ANTENA_ESTAVEL = Tendencia(intervalo=(70, 100), estado_alvo=Estado.ESTAVEL)
    BEAM_STEERING_CRITICA = Tendencia(intervalo=(0, 50), estado_alvo=Estado.CRITICO)
    BEAM_STEERING_ATENCAO = Tendencia(intervalo=(50, 70), estado_alvo=Estado.ATENCAO)
    BEAM_STEERING_ESTAVEL = Tendencia(intervalo=(70, 100), estado_alvo=Estado.ESTAVEL)
    CARGA_TERMICA_CRITICA = Tendencia(intervalo=(80, 100), estado_alvo=Estado.CRITICO)
    CARGA_TERMICA_ATENCAO = Tendencia(intervalo=(60, 80), estado_alvo=Estado.ATENCAO)
    CARGA_TERMICA_ESTAVEL = Tendencia(intervalo=(0, 60), estado_alvo=Estado.ESTAVEL)


class Satelite(BaseModel):
    regioes: list[EstadoBrasileiro]
    nome: str
    descricao: str
    energia: int = random.randint(20, 100)
    temperatura: int = random.randint(20, 80)
    comunicacao: int = random.randint(30, 100)
    latencia: int = random.randint(10, 200)
    throughput: int = random.randint(0, 200)
    saude_antena: int = random.randint(0, 100)
    beam_steering: int = random.randint(0, 100)
    carga_termica: int = random.randint(30, 150)
    tendencia_energia: Tendencias = Tendencias.ENERGIA_ESTAVEL
    tendencia_temperatura: Tendencias = Tendencias.TEMPERATURA_ESTAVEL
    tendencia_comunicacao: Tendencias = Tendencias.COMUNICACAO_ESTAVEL
    tendencia_latencia: Tendencias = Tendencias.LATENCIA_ESTAVEL
    tendencia_throughtput: Tendencias = Tendencias.THROUGHPUT_ESTAVEL
    tendencia_saude_antena: Tendencias = Tendencias.SAUDE_ANTENA_ESTAVEL
    tendencia_beam_steering: Tendencias = Tendencias.BEAM_STEERING_ESTAVEL
    tendencia_carga_termica: Tendencias = Tendencias.CARGA_TERMICA_ESTAVEL
    
    


# satelites: = Satelite(
#     regioes=[EstadoBrasileiro.ACRE, EstadoBrasileiro.AMAPA, EstadoBrasileiro.AMAZONAS],
#     nome="Amazonia l3",
#     descricao="Satelite voltado a fornecer internet para os estados da região da Amazônia Legal",
# )
satelites: list[Satelite] = [
    Satelite(
        regioes=[
            EstadoBrasileiro.PERNAMBUCO,
            EstadoBrasileiro.BAHIA,
            EstadoBrasileiro.SERGIPE,
            EstadoBrasileiro.ALAGOAS,
            EstadoBrasileiro.PARAIBA,
        ],
        nome="litoral nd1",
        descricao="satelite voltado a região litoranea do nordeste",
    ),
    Satelite(
        regioes=[
            EstadoBrasileiro.ACRE,
            EstadoBrasileiro.AMAPA,
            EstadoBrasileiro.AMAZONAS,
        ],
        nome="Amazonia l2",
        descricao="Satelite voltado a fornecer internet para os estados da região da Amazônia Legal",
    ),
    Satelite(
        regioes=[
            EstadoBrasileiro.SAO_PAULO,
            EstadoBrasileiro.MINAS_GERAIS,
        ],
        nome="cafeite sr9",
        descricao="Satelite voltado a fornecer internet para os estados de Minas Gerais e São Paulo devido a serem regiões de maior demanda, tem nome referente as politicas de cafe com leite",
    ),
    Satelite(
        regioes=[
            EstadoBrasileiro.MATO_GROSSO,
            EstadoBrasileiro.MATO_GROSSO_DO_SUL,
            EstadoBrasileiro.GOIAS,
        ],
        nome="Pantanal p4",
        descricao="Satelite voltado a fornecer conectividade de comunidades isoladas e monitoramento ambiental do Pantanal",
    ),
    Satelite(
        regioes=[
            EstadoBrasileiro.PARANA,
            EstadoBrasileiro.SANTA_CATARINA,
            EstadoBrasileiro.RIO_GRANDE_SUL,
        ],
        nome="Araucaria s5",
        descricao="Satelite voltado a fornecer conectividade e monitoramento ambiental da região do sul",
    ),
    Satelite(
        regioes=[
            EstadoBrasileiro.RIO_JANEIRO,
            EstadoBrasileiro.ESPIRITO_SANTO,
        ],
        nome="Cristo j3",
        descricao="Satelite voltado a fornecer conectividade aos estados do Rio de Janeiro e Espirito Santo",
    ),
]


class DataBase(BaseModel):
    atual: int = 0
    satelites: list[Satelite] = satelites

    @staticmethod
    def instancia():
        return database


database: DataBase = DataBase()
