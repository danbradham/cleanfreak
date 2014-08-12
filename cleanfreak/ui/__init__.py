from .ui import UI
from .mayaui import MayaUI


CONTEXTS = {
    "DEFAULT": UI,
    "MAYA": MayaUI,
}


def get(context):
    context = context.upper()
    try:
        return CONTEXTS.get(context)
    except KeyError:
        raise KeyError("UI Context does not exist for: {0}".format(context))
