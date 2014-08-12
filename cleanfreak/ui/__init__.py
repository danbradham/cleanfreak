from .ui import UI
from .mayaui import MayaUI


CONTEXTS = {
    "DEFAULT": UI,
    "MAYA": MayaUI,
}


def get(context):
    global CONTEXTS
    return CONTEXTS.get(context.upper(), CONTEXTS.get("DEFAULT"))
