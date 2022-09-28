import inspect
import cogpyt
from IPython.display import display, Markdown


def show_implementation(function):
    source = _get_source(function)

    display(
        Markdown(
            f'```py\n{source}\n```'
        )
    )


def get_function_from_source(source, name):
    scope = {}
    exec(source, scope)
    return scope[name]


def _get_source(function):
    if isinstance(function, str):
        return function
    elif isinstance(function, cogpyt.GeneratedFunction):
        return inspect.getsource(function.generator_function)
    else:
        return inspect.getsource(function)
