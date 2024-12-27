from types import FrameType
from .models import VarsDictAndLineNumberPair

def handle_frame(currentframe: FrameType) -> VarsDictAndLineNumberPair:
    from default_deepcopy import default_deepcopy
    items: dict = {
        k: default_deepcopy(v) 
        for k,v in 
        currentframe.f_locals.items()
        if k[0] != "_"
    }
    return VarsDictAndLineNumberPair(items, currentframe.f_lineno)