from .ui import UI
from .maya import MayaUI


CONTEXTS = {
    "default": UI,
    "maya": MayaUI,
}


def get(context):
    global CONTEXTS
    return CONTEXTS.get(context, "default")
