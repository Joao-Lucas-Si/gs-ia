from pydantic import BaseModel, ConfigDict

from src import data
from src.data import DataBase


class Telemetria(BaseModel):
    # model_config = ConfigDict(alias_generator=lambda name: name.replace("_", " "))
    temperatura: int
    energia: int
    comunicacao: int
    latencia: int
    throughput: int
    sauda_antena: int
    beam_steering: int
    carga_termica: int

    @staticmethod
    def coletar():
        db = DataBase.instancia()
        database = db.satelites[db.atual]
        telemetria = Telemetria(
            latencia=database.latencia,
            beam_steering=database.beam_steering,
            carga_termica=database.carga_termica,
            sauda_antena=database.saude_antena,
            throughput=database.throughput,
            temperatura=database.temperatura,
            energia=database.energia,
            comunicacao=database.comunicacao,
        )

        return telemetria
