
from .manager import info_manager

__info__ = info_manager(
    project = "PyCAMIA",
    package = "<main>",
    author = "Yuncheng Zhou",
    create = "2021-12",
    fileinfo = "Uncategorized features, not included in the main package.",
    help = "Use `pycamia.more` to call the functions. "
)

__all__ = """
    once
    void
    random_seed
""".split()

import sys

class Void: ...
void = Void()

class OnceError(Exception):
    pass

class Once:

    def __init__(self):
        self.history = set()
        self._disabled = False

    def filename_and_linenu(self):
        try:
            raise Exception
        except:
            f = sys.exc_info()[2].tb_frame.f_back.f_back
        return (f.f_code.co_filename, f.f_lineno)

    def enable(self):
        self._disabled = False

    def disable(self):
        self._disabled = True

    def __bool__(self):
        if self._disabled:
            return False
        f_name, l_nu = self.filename_and_linenu()
        if (f_name, l_nu) in self.history:
            return False
        self.history.add((f_name, l_nu))
        return True

once = Once()

def random_seed(seed):
    import random
    import numpy
    import batorch
    import torch
    random.seed(seed)
    numpy.random.seed(seed)
    batorch.manual_seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic=True
    torch.backends.cudnn.benchmark = True
