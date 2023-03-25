import importlib
from . import core, tests

importlib.reload(core)
importlib.reload(tests)