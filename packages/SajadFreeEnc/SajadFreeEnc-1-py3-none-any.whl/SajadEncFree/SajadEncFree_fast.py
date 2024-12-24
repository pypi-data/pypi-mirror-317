from . import SajadEncFree


def __getattr__(name):
    return getattr(SajadEncFree, name)
