import os
from ollama import Client
from dotenv import load_dotenv
from pathlib import Path

from rich.columns import Columns
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Column

from src.alertas import avaliar, ligarProtocolos
from src.constantes import Cores
from src.data import DataBase, Estado
from src.telemetria import Telemetria

load_dotenv()
# Identificação da trilha — ALTEREM conforme a escolha do grupo
TRILHA = "connectsat"
# "agrosat" | "envirosat" | "connectsat" | "mobilitysat"
client = Client(
    host="https://ollama.com",
    headers={"Authorization": "Bearer " + os.environ.get("OLLAMA_API_KEY", "")},
)


def render(output: str):
    parsed = Markdown(output)
    console = Console()
    console.print(parsed)


def llm(prompt, system=None, max_tokens=800, temperature=0.3):
    """Envia prompt ao gpt-oss:120b via Ollama Cloud."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    try:
        return client.chat(
            model="gpt-oss:120b",
            messages=messages,
            options={"num_predict": max_tokens, "temperature": temperature},
            stream=False,
        )["message"]["content"].strip()
    except Exception as e:
        return f"⚠ Erro ao consultar IA: {e}"


def load_system_prompt():
    """Lê o system prompt do arquivo prompts/system_prompt.md"""
    path = Path("prompts/system_prompt.md")
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "Você é um assistente."
    # fallback genérico


class MissionEngine:
    """Motor de análise — vocês completam os métodos abaixo."""

    def __init__(self):
        self.trilha = TRILHA
        self.system_prompt = load_system_prompt()

    def is_ready(self):  # Troquem para True quando analyze() estiver implementado
        return True

    def mostrarSatelites(self):
        console = Console()
        satelites = DataBase.instancia().satelites
        console.print(
            Columns(
                [
                    Panel(
                        f"{satelite[0] + 1}. {satelite[1].nome}\n{', '.join(map(lambda regiao: regiao.value, satelite[1].regioes))}",
                        expand=True,
                        border_style=Cores.corPrimaria,
                    )
                    for satelite in enumerate(satelites)
                ]
            )
        )

    def status_snapshot(self):
        """Retorna texto resumindo o estado atual da telemetria."""  # TODO: chamar telemetria.coletar() e formatar legivelmente
        db = DataBase.instancia()
        satelite = db.satelites[db.atual]
        dados = Telemetria.coletar()
        alertas = avaliar(dados)
        protocolos = ligarProtocolos(alertas)
        return f"""
# {db.satelites[db.atual].nome}
aperte enter para desativar o monitoramento de status
## dados
| Parametro | Valor | Estado| Tendencia|
|-----------|-------|-------|----------|
| temperatura| {dados.temperatura}| {alertas.temperatura.value}|{satelite.tendencia_temperatura.value.estado_alvo.value}|
| comunicação| {dados.comunicacao}|{alertas.comunicacao.value}|{satelite.tendencia_comunicacao.value.estado_alvo.value}|
| energia| {dados.energia}|{alertas.energia.value}|{satelite.tendencia_energia.value.estado_alvo.value}|
| beam steering|{dados.beam_steering}|{alertas.beam_steering.value}|{satelite.tendencia_beam_steering.value.estado_alvo.value}|
| latência| {dados.latencia}|{alertas.latencia.value}|{satelite.tendencia_latencia.value.estado_alvo.value}|
| throughput| {dados.throughput}|{alertas.throughput.value}|{satelite.tendencia_throughtput.value.estado_alvo.value}|
| carga termica| {dados.carga_termica}|{alertas.carga_termica.value}|{satelite.tendencia_carga_termica.value.estado_alvo.value}|
| saude antena| {dados.sauda_antena}|{alertas.sauda_antena.value}|{satelite.tendencia_saude_antena.value.estado_alvo.value}|


## protocolos automaticos

{'\n'.join(map(lambda protocolo: f"- {protocolo}", protocolos)) if len(protocolos) > 0 else "nenhum protocolo foi iniciado"}

"""

    def analyze(self, pergunta_usuario):
        """Analisa a pergunta com base na telemetria + alertas + IA."""  # TODO (foco do trabalho):
        dados = Telemetria.coletar()
        alertas = avaliar(dados)
        protocolos = ligarProtocolos(alertas)
        banco = DataBase.instancia()
        prompt = f"""
[todos os sátelites da rede]
{"\n---\n".join([f"""nome: {satelite.nome}
regiões: {', '.join(map(lambda regiao: regiao.value, satelite.regioes))}
descrição: {satelite.descricao}""" for satelite in banco.satelites])}
[sátelite monitorado]
{banco.satelites[banco.atual].nome}
[dados]
{dados.model_dump_json()}

[alerta]
{alertas.model_dump_json()}

[protocolos]
{'\n'.join(map(lambda protocolo: f"- {protocolo}", protocolos)) if len(protocolos) > 0 else "nenhum protocolo foi iniciado"}

[prompt do usuário]
{pergunta_usuario}
        """
        resposta = llm(prompt, load_system_prompt())
        # 1. Coletar dados via src.telemetria.coletar()
        # 2. Avaliar alertas via src.alertas.avaliar(dados)
        # 3. Montar prompt com dados + alertas + pergunta
        # 4. Chamar llm(prompt, system=self.system_prompt)
        # 5. Retornar a resposta
        return resposta
