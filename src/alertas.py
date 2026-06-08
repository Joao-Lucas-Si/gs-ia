


from pydantic import BaseModel
import pyfiglet
from rich.align import Align
from rich.console import Console
from rich.text import Text

from src.data import Estado
from src.telemetria import Telemetria


def alerta_critico():
    console = Console()   
    alerta =  pyfiglet.figlet_format("CRITICO", font="3d-ascii")
    console.print(Align.center(Text(alerta, style="bold #FF0000")))

class EstadoGeral(BaseModel):
    temperatura: Estado = Estado.ESTAVEL
    energia: Estado = Estado.ESTAVEL
    comunicacao: Estado = Estado.ESTAVEL
    latencia: Estado = Estado.ESTAVEL
    throughput: Estado = Estado.ESTAVEL
    sauda_antena: Estado = Estado.ESTAVEL
    beam_steering: Estado = Estado.ESTAVEL
    carga_termica: Estado = Estado.ESTAVEL
    
def ligarProtocolos(alertas: EstadoGeral):
    protocolos = []
    if alertas.temperatura == Estado.CRITICO:
        protocolos.append("Superaquecimento, Ativando resfrigerador")
    if alertas.energia == Estado.CRITICO:
        protocolos.append("Energia escassa, ligando gerador")
    if alertas.comunicacao == Estado.CRITICO:
        protocolos.append("Comunicação critica, procurando canal estavel")
        
    return protocolos

def avaliar(dados: Telemetria):
    geral= EstadoGeral()
    if dados.temperatura > 60:
        geral.temperatura = Estado.CRITICO
    elif dados.temperatura > 40 and dados.temperatura <= 60:
        geral.temperatura = Estado.ATENCAO
        
    if dados.comunicacao < 50:
        geral.comunicacao = Estado.CRITICO
    elif dados.comunicacao < 70:
        geral.comunicacao = Estado.ATENCAO
    
    if dados.energia < 30:
        geral.energia = Estado.CRITICO
    elif dados.energia < 60:
        geral.energia = Estado.ATENCAO
    
    if dados.latencia > 150:
        geral.latencia = Estado.CRITICO
    elif dados.latencia > 80 and dados.latencia <= 150:
        geral.latencia = Estado.ATENCAO
    
    if dados.throughput < 50:
        geral.throughput = Estado.CRITICO
    elif dados.throughput >= 50 and dados.throughput < 100:
        geral.throughput = Estado.ATENCAO
    
    if dados.sauda_antena < 50:
        geral.sauda_antena = Estado.CRITICO
    elif dados.sauda_antena >= 50 and dados.sauda_antena < 70:
        geral.sauda_antena = Estado.ATENCAO
    
    if dados.beam_steering < 50:
        geral.beam_steering = Estado.CRITICO
    elif dados.beam_steering >= 50 and dados.beam_steering < 70:
        geral.beam_steering = Estado.ATENCAO
    
    if dados.carga_termica > 80:
        geral.carga_termica = Estado.CRITICO
    elif dados.carga_termica > 60 and dados.carga_termica <= 80:
        geral.carga_termica = Estado.ATENCAO
        
    return geral