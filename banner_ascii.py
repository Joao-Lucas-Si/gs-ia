import pyfiglet
from rich.console import Console
from rich.align import Align
from rich.text import Text

def gerar_banner(fonte: str = "ansi_shadow", texto: str = "Mission Control AI"):
    console = Console()
    # Gera as duas linhas do banner em ASCII art
    linha1 = pyfiglet.figlet_format("Global Solution", font=fonte)
    linha2 = pyfiglet.figlet_format(texto, font=fonte)
    # Pinta em ciano (estilo Claude Code) e centraliza
    console.print(Align.center(Text(linha1, style="bold #A855F7")))
    console.print(Align.center(Text(linha2, style="bold #06B6D4")))
    console.print(
        Align.center(
            Text("── 2026.1 · Prompt Engineering and AI · FIAP ──", style="italic #8484A0")
        )
    )

if __name__ == "__main__":
    gerar_banner()
    