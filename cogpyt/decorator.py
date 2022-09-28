"""
Contains the functionality for the library's decorator.
Naming might be suboptimal, but, did I say this is a POC?
"""


import inspect
from typing import Callable
from .context import GeneratedCodeBlock


class GeneratedFunction:
    """
    Represents the generated function.
    You can call it directly, or use `get_source()`
    to investigate the generated source and debug it.
    """
    def __init__(self, func: Callable):
        self._generator_function = func
        self._signature = self._get_signature(func)
        self._name = func.__name__

    @property
    def name(self):
        return self._name

    @property
    def generator_function(self):
        return self._generator_function

    @classmethod
    def _get_signature(cls, func):
        # includes the generated_code_block parameter for code generation
        # as can be seen in `get_source()`
        modified_signature = inspect.signature(func)

        modified_parameters = modified_signature.parameters
        tail_parameters = list(modified_parameters)[1:]
        # also, remove any signatures, since these aren't really handled
        # perfectly in python yet...
        original_parameters = [
            modified_parameters[p].replace(annotation=inspect.Signature.empty)
            for p in tail_parameters
        ]

        return modified_signature.replace(
            parameters=original_parameters,
            return_annotation=inspect.Signature.empty,
        )

    def __call__(self, *args, **kwargs) -> any:
        scope = {}
        source = self.get_source(*args, **kwargs)
        # sure, project is a HACK.
        # Wouldn't be writing this at 3AM if it wasn't.
        # pylint: disable=exec-used
        exec(source, scope)
        return scope[self._name](*args, **kwargs)

    def get_source(self, *args, **kwargs) -> str:
        """
        Returns
        -------
        The generated Python source code for
        the given set of arguments.
        """
        argument_names = list(self._signature.parameters.keys())
        generated_code_block = GeneratedCodeBlock(
            outer_indentation=True,
            banned_locals=argument_names
        )
        self.generator_function(generated_code_block, *args, **kwargs)

        return '\n'.join([
            f'def {self._name}{self._signature}:',
            generated_code_block.export()
        ])
