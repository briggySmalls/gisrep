"""Package for girep output classes
"""

from .stdout import StdOutOutput
from .clipboard import ClipboardOutput
from .file import FileOutput

__all__ = ['StdOutOutput', 'ClipboardOutput', 'FileOutput']
