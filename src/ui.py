import random
from time import sleep

from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding import KeyBindings
from rich.align import Align
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.padding import Padding
from rich.panel import Panel
from rich.text import Text
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
import pyfiglet
from datetime import datetime

from src.constantes import Cores
from src.data import DataBase, Tendencias
from src.engine import MissionEngine
from src.utils import Temporizador


console = Console()
session = PromptSession(style=Style.from_dict({"prompt": f"{Cores.corPrimaria} bold"}))


def show_banner():
    """Exibe banner ASCII colorido no início."""
    banner = pyfiglet.figlet_format("Mission Control", font="ansi_shadow")
    console.print(Align.center(Text(banner, style="bold #06B6D4")))
    console.print(
        Align.center(
            Panel.fit(
                "Sistema de monitoramento e análise por IA generativa.\n"
                "Use /help para ver os comandos · /exit para sair.\n"
                "Modelo: gpt-oss:120b via Ollama Cloud",
                title="◆ MISSION CONTROL",
                border_style=Cores.corPrimaria,
            )
        )
    )


def create_response(text):
    """Renderiza resposta da IA em painel com timestamp."""
    now = datetime.now().strftime("%H:%M")
    markdown = Markdown(text)
    # console.print(
    painel = Panel(
        markdown,
        expand=False,
        padding=(0, 2),
        width=100,
        title="◆ Mission Control",
        subtitle=now,
        border_style=Cores.corPrimaria
    )
    painel.box
    return Align.center(painel)


def show_response(text):
    console.print(create_response(text))


def iniciar():
    db = DataBase.instancia()

    def modificarTendencias():
        for satelite in db.satelites:
            satelite.tendencia_energia = [
                Tendencias.ENERGIA_ESTAVEL,
                Tendencias.ENERGIA_ATENCAO,
                Tendencias.ENERGIA_CRITICA,
            ][random.randint(0, 2)]
            satelite.tendencia_temperatura = [
                Tendencias.TEMPERATURA_ESTAVEL,
                Tendencias.TEMPERATURA_ATENCAO,
                Tendencias.TEMPERATURA_CRITICA,
            ][random.randint(0, 2)]
            satelite.tendencia_comunicacao = [
                Tendencias.COMUNICACAO_ESTAVEL,
                Tendencias.COMUNICACAO_ATENCAO,
                Tendencias.COMUNICACAO_CRITICA,
            ][random.randint(0, 2)]
            satelite.tendencia_latencia = [
                Tendencias.LATENCIA_ESTAVEL,
                Tendencias.LATENCIA_ATENCAO,
                Tendencias.LATENCIA_CRITICA,
            ][random.randint(0, 2)]
            satelite.tendencia_saude_antena = [
                Tendencias.SAUDE_ANTENA_ESTAVEL,
                Tendencias.SAUDE_ANTENA_ATENCAO,
                Tendencias.SAUDE_ANTENA_CRITICA,
            ][random.randint(0, 2)]
            satelite.tendencia_beam_steering = [
                Tendencias.BEAM_STEERING_ESTAVEL,
                Tendencias.BEAM_STEERING_ATENCAO,
                Tendencias.BEAM_STEERING_CRITICA,
            ][random.randint(0, 2)]
            satelite.tendencia_throughtput = [
                Tendencias.THROUGHPUT_ESTAVEL,
                Tendencias.THROUGHPUT_ATENCAO,
                Tendencias.THROUGHPUT_CRITICA,
            ][random.randint(0, 2)]
            satelite.tendencia_carga_termica = [
                Tendencias.CARGA_TERMICA_ESTAVEL,
                Tendencias.CARGA_TERMICA_ATENCAO,
                Tendencias.CARGA_TERMICA_CRITICA,
            ][random.randint(0, 2)]

    def aplicarTendencia():
        for satelite in db.satelites:
            satelite.energia = satelite.tendencia_energia.value.afetar(satelite.energia)
            satelite.temperatura = satelite.tendencia_temperatura.value.afetar(
                satelite.temperatura
            )
            satelite.beam_steering = satelite.tendencia_beam_steering.value.afetar(
                satelite.beam_steering
            )
            satelite.latencia = satelite.tendencia_latencia.value.afetar(
                satelite.latencia
            )
            satelite.comunicacao = satelite.tendencia_comunicacao.value.afetar(
                satelite.comunicacao
            )
            satelite.saude_antena = satelite.tendencia_saude_antena.value.afetar(
                satelite.saude_antena
            )
            satelite.throughput = satelite.tendencia_throughtput.value.afetar(
                satelite.throughput
            )
            satelite.carga_termica = satelite.tendencia_carga_termica.value.afetar(
                satelite.carga_termica
            )

    incremental = Temporizador(aplicarTendencia, 1)
    incremental.start()
    
    tendencias = Temporizador(modificarTendencias, 5 * 60)
    tendencias.start()


keyboard = KeyBindings()

sugestoes = WordCompleter(
    ["/status", "/trocar", "/satelites", "/alterar", "/alterar-estavel", "/alterar-critico", "/alterar-atencao", "/clear", "/exit", "/about", "/help"]
)




def run_cli(engine: MissionEngine):
    """Loop principal da CLI."""
    db = DataBase.instancia()
    lives: list[Live] = []
    show_banner()
    if not engine.is_ready():
        console.print(" ⚠ Engine status: AGUARDANDO IMPLEMENTAÇÃO ✗\n", style="yellow")
    iniciar()
    user_input = ""
    while True:
        try:
            session.prompt_continuation
            user_input = session.prompt("❯ ", completer=sugestoes).strip()
        except (KeyboardInterrupt, EOFError):
            break
        if not user_input:
            continue
        if user_input == "/exit":
            break
        if user_input == "/satelites":
            engine.mostrarSatelites()
            continue
        if user_input == "/alterar-estavel":
            satelite = db.satelites[db.atual]
            satelite.tendencia_energia = Tendencias.ENERGIA_ESTAVEL
            satelite.tendencia_temperatura = Tendencias.TEMPERATURA_ESTAVEL
            satelite.tendencia_comunicacao = Tendencias.COMUNICACAO_ESTAVEL
            satelite.tendencia_latencia = Tendencias.LATENCIA_ESTAVEL
            satelite.tendencia_saude_antena = Tendencias.SAUDE_ANTENA_ESTAVEL
            satelite.tendencia_beam_steering = Tendencias.BEAM_STEERING_ESTAVEL
            satelite.tendencia_throughtput = Tendencias.THROUGHPUT_ESTAVEL
            satelite.tendencia_carga_termica = Tendencias.CARGA_TERMICA_ESTAVEL
            print("todos os parametros foram alterados para estavel")
            continue
        if user_input == "/alterar-atencao":
            satelite = db.satelites[db.atual]
            satelite.tendencia_energia = Tendencias.ENERGIA_ATENCAO
            satelite.tendencia_temperatura = Tendencias.TEMPERATURA_ATENCAO
            satelite.tendencia_comunicacao = Tendencias.COMUNICACAO_ATENCAO
            satelite.tendencia_latencia = Tendencias.LATENCIA_ATENCAO
            satelite.tendencia_saude_antena = Tendencias.SAUDE_ANTENA_ATENCAO
            satelite.tendencia_beam_steering = Tendencias.BEAM_STEERING_ATENCAO
            satelite.tendencia_throughtput = Tendencias.THROUGHPUT_ATENCAO
            satelite.tendencia_carga_termica = Tendencias.CARGA_TERMICA_ATENCAO
            print("todos os parametros foram alterados para atenção")
            continue
        if user_input == "/alterar-critico":
            satelite = db.satelites[db.atual]
            satelite.tendencia_energia = Tendencias.ENERGIA_CRITICA
            satelite.tendencia_temperatura = Tendencias.TEMPERATURA_CRITICA
            satelite.tendencia_comunicacao = Tendencias.COMUNICACAO_CRITICA
            satelite.tendencia_latencia = Tendencias.LATENCIA_CRITICA
            satelite.tendencia_saude_antena = Tendencias.SAUDE_ANTENA_CRITICA
            satelite.tendencia_beam_steering = Tendencias.BEAM_STEERING_CRITICA
            satelite.tendencia_throughtput = Tendencias.THROUGHPUT_CRITICA
            satelite.tendencia_carga_termica = Tendencias.CARGA_TERMICA_CRITICA
            print("todos os parametros foram alterados para critico")
            continue
        if user_input == "/alterar":
            console.print("escolha a tendencia a ser alterada")
            aspecto = 0
            nivel = 0
            while True:
                console.print(Markdown("""1. energia 
2. temperatura
3. comunicacao
4. beam steering
5. latência
6. throughput
7. carga termica
8. saude da antena"""))
                aspecto = int(session.prompt("> ", completer=WordCompleter(["1", "2", "3", "4","5", "6", "7", "8"])))
                
                if aspecto > 0 and aspecto <= 8:
                    break
            
                console.print("valor invalido", style=f"bold {Cores.corErro}")
    
            console.print("escolha a tendencia")
            while True:
                console.print("1. Estavel\n2. Atenção\n3. Critico")
                
                nivel = int(session.prompt("> "))
                
                if 0 < nivel <= 3:
                    break
                
                console.print("valor invalido", style=f"bold {Cores.corErro}")
            satelite = db.satelites[db.atual]
            match (aspecto):        
                case 1:
                    satelite.tendencia_energia = [Tendencias.ENERGIA_ESTAVEL, Tendencias.ENERGIA_ATENCAO, Tendencias.ENERGIA_CRITICA][nivel - 1]
                case 2:
                    satelite.tendencia_temperatura = [Tendencias.TEMPERATURA_ESTAVEL, Tendencias.TEMPERATURA_ATENCAO, Tendencias.TEMPERATURA_CRITICA][nivel - 1]
                case 3:
                    satelite.tendencia_comunicacao = [Tendencias.COMUNICACAO_ESTAVEL, Tendencias.COMUNICACAO_ATENCAO, Tendencias.COMUNICACAO_CRITICA][nivel - 1]
                case 4:
                    satelite.tendencia_beam_steering = [Tendencias.BEAM_STEERING_ESTAVEL, Tendencias.BEAM_STEERING_ATENCAO, Tendencias.BEAM_STEERING_CRITICA][nivel - 1]
                case 5:
                    satelite.tendencia_latencia = [Tendencias.LATENCIA_ESTAVEL, Tendencias.LATENCIA_ATENCAO, Tendencias.LATENCIA_CRITICA][nivel - 1]
                case 6:
                    satelite.tendencia_throughtput = [Tendencias.THROUGHPUT_ESTAVEL, Tendencias.THROUGHPUT_ATENCAO, Tendencias.THROUGHPUT_CRITICA][nivel - 1]
                case 7:
                    satelite.tendencia_saude_antena = [Tendencias.SAUDE_ANTENA_ESTAVEL, Tendencias.SAUDE_ANTENA_ATENCAO, Tendencias.SAUDE_ANTENA_CRITICA][nivel - 1]
                case 8:
                    satelite.tendencia_carga_termica = [Tendencias.CARGA_TERMICA_ESTAVEL, Tendencias.CARGA_TERMICA_ATENCAO, Tendencias.CARGA_TERMICA_CRITICA][nivel - 1]
            continue
        if user_input == "/trocar":
            engine.mostrarSatelites()
            alvo = session.prompt("número do satelite alvo > ").strip()
            db.atual = int(alvo) - 1
            continue
        if user_input == "/help":
            console.print(
                # Markdown(
                """painel de ajuda                    
Comandos: /help /satelite /monitorar /status /about /clear /exit
                
 - /help: ajuda e descrição de comandos
 - /satelite: listagem de satelites em atividade na rede
 - /trocar: escolha do satelite atual
 - /alterar: mudar têndencias de um unico parametro
 - /alterar-estavel: muda todas as têndencias para estado estavel
 - /alterar-atencao: muda todas as têndencias para estado atenção
 - /alterar-critico: muda todas as têndencias para estado critico
 - /status: tabela informativa sobre o sátelite atual
 - /about: descrição do projeto
 - /clear: limpeza do console
 - /exit - sair do painel de controle
                """,
                # )
            )
            continue
        if user_input == "/status":
            text = engine.status_snapshot()
            continuar = True

            @keyboard.add("enter")
            def parar(event):
                nonlocal continuar
                continuar = False

            painel = Live(create_response(text), refresh_per_second=4)
            painel.start()

            def atualizar():
                painel.update(create_response(engine.status_snapshot()))
                painel.refresh()

            temporizador = Temporizador(atualizar, 0.5)
            temporizador.start()
            input()

            painel.stop()
            temporizador.parar()

            continue

        if user_input == "/clear":
            console.clear()
            show_banner()
            continue  # Qualquer outra entrada vai para o motor de análise
        if user_input.startswith("/"):
            console.print(Text(f"comando {user_input} invalido", style=f"bold {Cores.corErro}"))
            continue
        resposta = engine.analyze(user_input)
        show_response(resposta)
