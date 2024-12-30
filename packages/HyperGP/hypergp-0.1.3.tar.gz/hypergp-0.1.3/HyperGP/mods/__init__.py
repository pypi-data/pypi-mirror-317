from .mod_base import ModBase
from . import tree2graph_transformer
from .multiprocess_parallel import MultiProcess


class AvailableMods:
    parallel: MultiProcess = MultiProcess

class __Mods:
    parallel: MultiProcess = MultiProcess()

