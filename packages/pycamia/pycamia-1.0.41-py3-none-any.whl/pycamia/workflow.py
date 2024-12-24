
from .manager import info_manager

__info__ = info_manager(
    project = "PyCAMIA",
    package = "<main>",
    author = "Yuncheng Zhou",
    create = "2024-09",
    fileinfo = "File to set workflows."
)

__all__ = """
    scope
    Jump
    jump
    Workflow
    Switch
    switch
""".split()

from .timing import Timer
from .exception import Error
from .decorators import alias

class Jump(object):
    """
    Creates a Jump Error to escape scopes. 

    Examples::
        >>> with scope("test"), jump:
        ...     # inside codes
        ... 
        # nothing, the inside codes do not run
        >>> with scope("test"), Jump(False) as stop:
        ...     print("Part I")
        ...     stop()
        ...     print("Part II")
        ... 
        Part I
    """
    def __init__(self, jump=None): self.jump = True if jump is None else jump
    def __enter__(self):
        def dojump(): raise Error("Jump")("Jump by class 'Jump'. ")
        if self.jump: dojump()
        else: return dojump
    def __exit__(self, *args): pass
    def __call__(self, condition): return Jump(condition)
    
def scope(name, log_on_screen=True):
    """
    An allias of timer to better organize the codes, use .exit() to exit the scope. 
    
    Args:
        name (str): the name of the scope, used to display. 
        log_on_screen (bool): whether to show the time span or not. 

    Examples::
        >>> with scope("test"):
        ...     # inside codes
        ... 
        # some outputs
        [scope test takes 0.001s]
        >>> with scope("this") as s:
        ...     print("Part I")
        ...     s.exit()
        ...     print("Part II")
        ...
        Part I
        >>> with scope("this again", False) as s:
        ...     print("Part I")
        ...     print("Part II")
        ...
        Part I
        Part II
        >>> print(s.recorded_time)
        2.86102294921875e-06
    """
    return Timer("scope " + str(name), timing=True, log_on_screen=log_on_screen)

jump = Jump()
"""
The jumper, one can use it along with `scope`(or `Timer`) to jump a chunk of codes. 
"""

class Workflow:
    """
    A structure to create a series of workflow. 
    
    Note:
        Remember to manually add a behaviour for each block: 
            '*.force_run' force the block to run, without checking the workflow.
            '*.force_skip'/'*.force_jump' force the block to be skipped, without checking the workflow.
            '*.use_tag'/'*.run_as_workflow' runs the block following the workflow schedule if one tag name is provided.
            '*.all_tags'/'*.run_if_all_tags_in_workflow' runs the block when all given tags are defined in the workflow. 
            '*.any_tag'/'*.run_if_any_tag_in_workflow' runs the block when at least one tag is defined in the workflow. 
        Fogetting to add the behaviour would result in an automatic run of blocks. See the example for details of bahaviours. 
    
    Args:
        *args: the list of scope names to run. 

    Examples::
        >>> run = Workflow("read data", "run method", "visualization")
        ... with run("read data"), run.use_tag:
        ...     print(1, end='')
        ... with run("pre-processing"), run.use_tag:
        ...     print(2, end='')
        ... with run("pre-processing", "run method"), run.all_tags:
        ...     print(3, end='')
        ... with run("visualization"), run.force_skip:
        ...     print(4, end='')
        ... 
        1[read data takes 0.000022s]
    """
    def force_jump(self): ...
    def run_as_workflow(self): ...
    def all_tags(self): ...
    def use_tag(self): ...
    def any_tag(self): ...
    def __init__(self, *args, verbose=True): self.workflow = args; self.verbose=verbose
    def __call__(self, *keys):
        if len(keys) == 1 and isinstance(keys[0], (list, tuple)): keys = keys[0]
        self.keys=keys
        return Timer(','.join(keys), timing=self.verbose)
    def __getattr__(self, *k): return self(*k)
    def __getitem__(self, *k): return self(*k)
    @property
    def force_run(self): return Jump(False)
    @alias("force_jump")
    @property
    def force_skip(self): return Jump(True)
    @alias("run_as_workflow", "all_tags", "use_tag")
    @property
    def run_if_all_tags_in_workflow(self):
        return Jump(any(k not in self.workflow for k in self.keys))
    @alias("any_tag")
    @property
    def run_if_any_tag_in_workflow(self):
        return Jump(all(k not in self.workflow for k in self.keys))

class Switch:
    """
    The replacement of C-styled switch in Python. 
    One can use the scope in the following 2 ways where #2 is more recommanded. 
    Example #1::
        >>> from pycamia import Switch
        >>> obj = 2
        >>> with Switch(obj) as case:
        ...     with case(1) as this:
        ... 	    assert this
        ... 	    print("hi")
        ...
        >>>     with case(2) as this:
        ... 	    assert this
        ... 	    print('bye')
        ...
        bye
    Example #2 (NOTE: switch[=Switch()] here is in lower cases. )::
        >>> from pycamia import switch
        >>> obj = 3
        >>> with switch:
	    ...     assert obj == 1
	    ...     print("hi")
        ...
        >>> with switch:
	    ...     assert obj == 2
	    ...     print('bye')
        ...
        >>> switch.close()
        Traceback (most recent call last):
            [...]
        pycamia.exception.SwitchError: No case matched. 
    """
    def __init__(self, variable=None, as_value=False):
        self.value = variable
        self.values = []
        self.as_value = as_value
        self.matched = False
    def __call__(self, value):
        self.values.append(value)
        if value == self.value:
            self.matched = True
        return Switch(value == self.value, as_value = True)
    def __enter__(self): return self.value if self.as_value else self
    def __exit__(self, error_type, error_msg, traceback):
        if error_type is None:
            if self.values: self.close()
            else: self.matched = True
            return True
        if error_type == Error("Jump") or error_type == AssertionError: return True
    @alias("end_switch")
    def close(self):
        if not self.matched:
            if self.value is not None:
                error_msg = f"Unrecognized case {self.value}"
                if self.values: error_msg += f", the available options are {self.values}. "
                else: error_msg += '. '
            else: error_msg = "No case matched. "
            raise Error("Switch")(error_msg)

switch = Switch()