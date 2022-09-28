"""
Cogpyt implements code generation in pure Python.
"""


from .__about__ import __title__, __author__, __description__
from .__about__ import __url__, __version__, __copyright__, __licence__
from .decorator import GeneratedFunction
from .context import GeneratedCodeBlock


__all__ = [
    '__title__',
    '__author__',
    '__description__',
    '__url__',
    '__version__',
    '__copyright__',
    '__licence__',
    'GeneratedFunction',
    'GeneratedCodeBlock',
]
