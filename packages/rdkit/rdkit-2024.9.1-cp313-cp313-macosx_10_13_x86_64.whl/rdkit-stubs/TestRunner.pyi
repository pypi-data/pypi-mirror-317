from __future__ import annotations
import os as os
import sys as sys
import typing
__all__ = ['BUILD_TYPE_ENVVAR', 'OutputRedirectC', 'isDebugBuild', 'os', 'redirect_stderr', 'redirect_stdout', 'sys']
class OutputRedirectC:
    """
    Context manager which uses low-level file descriptors to suppress
    output to stdout/stderr, optionally redirecting to the named file(s).
    
    Suppress all output
    with Silence():
      <code>
    
    Redirect stdout to file
    with OutputRedirectC(stdout='output.txt', mode='w'):
      <code>
    
    Redirect stderr to file
    with OutputRedirectC(stderr='output.txt', mode='a'):
      <code>
    http://code.activestate.com/recipes/577564-context-manager-for-low-level-redirection-of-stdou/
    >>>
    
    """
    __firstlineno__: typing.ClassVar[int] = 61
    __static_attributes__: typing.ClassVar[tuple] = ('combine', 'fds', 'mode', 'null_fds', 'null_streams', 'outfiles', 'saved_fds', 'saved_streams')
    def __enter__(self):
        ...
    def __exit__(self, *args):
        ...
    def __init__(self, stdout = '/dev/null', stderr = '/dev/null', mode = 'wb'):
        ...
class _RedirectStream:
    __firstlineno__: typing.ClassVar[int] = 24
    __static_attributes__: typing.ClassVar[tuple] = ('_new_target', '_old_targets')
    _stream = None
    def __enter__(self):
        ...
    def __exit__(self, exctype, excinst, exctb):
        ...
    def __init__(self, new_target):
        ...
class redirect_stderr(_RedirectStream):
    """
    Context manager for temporarily redirecting stderr to another file.
    """
    __firstlineno__: typing.ClassVar[int] = 56
    __static_attributes__: typing.ClassVar[tuple] = tuple()
    _stream: typing.ClassVar[str] = 'stderr'
class redirect_stdout(_RedirectStream):
    """
    Context manager for temporarily redirecting stdout to another file.
    
    # How to send help() to stderr
    with redirect_stdout(sys.stderr):
        help(dir)
    
    # How to write help() to a file
    with open('help.txt', 'w') as f:
        with redirect_stdout(f):
            help(pow)
    """
    __firstlineno__: typing.ClassVar[int] = 41
    __static_attributes__: typing.ClassVar[tuple] = tuple()
    _stream: typing.ClassVar[str] = 'stdout'
def isDebugBuild():
    ...
BUILD_TYPE_ENVVAR: str = 'RDKIT_BUILD_TYPE'
