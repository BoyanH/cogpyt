"""
Implements the functionality of the context manager
used for code generation.
Naming might be suboptimal, but, did I say this is a POC?
"""


import sys
import inspect
import ast
import copy
from typing import List, Dict, Union
from cogpyt.exception import SkipWithBlockException


class GeneratedCodeBlock:
    """
    TODO: interface documentation

    TODO: pass statements not removed, as not harmful.
    Feel free to contribute to resolve if it bothers you.
    """

    def __init__(
            self,
            indent: int = 4,
            outer_indentation: bool = False,
            banned_locals: List[str] = None
    ):
        """
        Parameters
        ----------
        indent
            amount of spaces to use for code indentation
        outer_indentation
            whether to indent the entire exported code.
            Useful to just append the generated code
            to a function definition header.
        banned_locals
            Local variables to never replace in generated code.
            Currently only used to prevent replacing method arguments in code.
        """
        # NOTE: indentation starts at 1 to export source which can be easily
        #       appended to a function definition. After all, this is POC
        self._indentation = 0
        self._spaces_per_indentation = indent
        self._outer_indentation = outer_indentation
        self._banned_locals = banned_locals or []
        self._generated_code = []

        self._old_trace = None
        self._filename = None
        self._source_ast_nodes_by_line = None
        self._current_block_start = None
        self._current_locals = None

    def __enter__(self):
        """
        Sets an exception to be executed next in the `with` block.
        This allows the code in the with block not to be executed,
        but instead to be extracted and enriched as generated code
        in the `__exit__` method. Also keeps track of the relevant
        context in the moment of execution to do so.
        """
        # prevent with block execution
        self._old_trace = sys.gettrace()
        sys.settrace(lambda *args, **keys: None)
        context_entering_frame = inspect.currentframe().f_back
        context_entering_frame.f_trace = self._trace

        # store information on where the source of the with block starts
        # and which local variables are available at the time of execution
        self._current_block_start = context_entering_frame.f_lineno
        self._current_locals = context_entering_frame.f_locals

        filename = context_entering_frame.f_code.co_filename
        if not self._filename:
            self._filename = filename
            self._source_ast_nodes_by_line = self._get_source_ast_node_by_line(
                filename
            )
        else:
            assert self._filename == filename, (
                'Expected a single code generation context '
                'instance to be used only '
                'within the same source code file.'
            )

    @classmethod
    def _get_source_ast_node_by_line(
            cls,
            filename: str
    ) -> Dict[int, ast.With]:
        """
        Returns a dictionary of (line number -> with statement AST).
        """
        ast_node_by_line = {}

        with open(filename, 'r', encoding='utf8') as file:
            source = file.read()

        source_ast = ast.parse(source)
        for node in ast.walk(source_ast):
            if isinstance(node, ast.With):
                line = node.lineno
                # We assume there can't be multiple `with`
                # statements defined on the same line
                assert line not in ast_node_by_line, (
                    'Multiple with statements on the same source line.'
                )
                ast_node_by_line[line] = node

        return ast_node_by_line

    def _trace(self, frame, event, arg):
        sys.settrace(self._old_trace)
        raise SkipWithBlockException()

    def __exit__(self, type_, value, traceback) -> bool:
        assert issubclass(type_, SkipWithBlockException)

        code_lines = self._extract_generated_code()
        self._generated_code.extend(code_lines)

        return True

    def _extract_generated_code(self) -> List[str]:
        """
        Extracts the generated code from the `with` statement
        marked by the `self._current_block_start` line in the
        abstract syntax tree of the source code file,
        available from `self._source_ast_nodes_by_line`.
        Also replaces any constants available as local constants
        from `self._current_locals`.

        Returns
        -------
        The so generated code.
        """
        with_node = self._source_ast_nodes_by_line[self._current_block_start]
        # The same line of the source can result in multiple lines
        # in the generated code. Handle each one separately (i.e. copy).
        with_node_copy = copy.deepcopy(with_node)
        code_ast = ast.Module(with_node_copy.body, [])

        inline_locals_transform = _InlineLocalsNodeTransformer(
            self._current_locals,
            self._banned_locals,
        )
        inline_locals_transform.visit(code_ast)

        code_lines = ast.unparse(code_ast).split('\n')
        return self._indent_lines(code_lines, self._indentation)

    def _indent_lines(self, lines: List[str], indentation: int) -> List[str]:
        indentation_string = ' ' * indentation * self._spaces_per_indentation
        return [
            indentation_string + line
            for line in lines
        ]

    @classmethod
    def _transform_into_generated_code(
            cls,
            source: str,
            indentation: int
    ) -> List[str]:
        pass

    def indent(self, amount: int = 1):
        """
        Increments the indentation level of the following
        generated code.
        """
        self._verify_indentation_amount(amount)
        self._indentation += amount

    def dedent(self, amount: int = 1):
        """
        Decrements the indentation level of the following
        generated code.
        """
        self._verify_indentation_amount(amount)

        if self._indentation < amount:
            raise ValueError('Cannot dedent past minimum indentation!')

        self._indentation -= amount

    @classmethod
    def _verify_indentation_amount(cls, amount):
        assert amount > 0, 'Indentation amount needs to be positive'
        assert type(amount) == int, 'Indentation amount needs to be an integer'

    def export(self) -> str:
        """
        Returns
        -------
        The source code generated thus far.
        """
        code = self._generated_code
        if self._outer_indentation:
            code = self._indent_lines(code, 1)

        return '\n'.join(code)


class _InlineLocalsNodeTransformer(ast.NodeTransformer):
    """
    Replaces all variables (ast.Name), which have defined substitutable values
    in the local variables scope, with constants (ast.Constant).
    This allows constants to be hard-coded in the generated code.
    A value is considered substitutable if it can be represented as
    a literal in pure python code.
    """
    def __init__(self, locals_: dict, banned_locals: List[str]):
        self.locals = {
            key: value
            for key, value in locals_.items()
            if key not in banned_locals and self.is_substitutable(value)
        }

    @classmethod
    def is_substitutable(cls, value) -> bool:
        """
        Returns
        -------
        Whether the value is substitutable directly in source code,
        i.e. whether it can be inlined.
        """
        try:
            # TODO: any better approach for this?
            # pylint: disable=eval-used
            eval(repr(value))
            return True
        except SyntaxError:
            return False

    # pylint: disable=invalid-name
    def visit_Name(self, name: ast.Name) -> Union[ast.Name, ast.Constant]:
        """
        Visitor method, this is the main workhorse.
        Replaces variables (names) with constants where possible.
        """
        if name.id in self.locals:
            value = self.locals[name.id]
            return ast.Constant(value)

        return name
