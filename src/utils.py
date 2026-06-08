from threading import Thread
from time import sleep
from typing import Any, Callable, Iterable, Mapping


class Temporizador(Thread):
    codigo: Callable[[], None]
    tempo: float
    
    def __init__(self, codigo: Callable[[], None], tempo: float, group: None = None, target: Callable[..., object] | None = None, name: str | None = None, args: Iterable[Any] = ..., kwargs: Mapping[str, Any] | None = None, *, daemon: bool | None = None) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.codigo = codigo
        self.tempo = tempo
    
    continuar = True
    
    def parar(self):
        self.continuar = False
    def run(self) -> None:
        while self.continuar:
            self.codigo()
            sleep(self.tempo)
    
    