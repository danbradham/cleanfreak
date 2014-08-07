from .ui import UI
from .maya import MayaUI


CONTEXTS = {
    "DEFAULT": UI,
    "MAYA": MayaUI,
}


def get(context):
    global CONTEXTS
    return CONTEXTS.get(context.upper(), CONTEXTS.get("DEFAULT"))
