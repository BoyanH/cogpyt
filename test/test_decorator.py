from typing import List
from itertools import count
import pytest
from cogpyt.decorator import GeneratedFunction
from cogpyt.context import GeneratedCodeBlock


# Not the cleanest, the wrapper is adding this argument.
# You should have come across the term POC in the project already ;)
# pylint: disable=no-value-for-parameter


def test_source_investigation():
    @GeneratedFunction
    def printer_method(
            generated_code_block: GeneratedCodeBlock,
            *print_texts: List[str],
    ):
        for text in print_texts:
            with generated_code_block:
                print(text)

    generated_code = printer_method.get_source(
        'Hello', 'code', 'generation', 'in', 'pure', 'Python', '!'
    )
    expected = '\n'.join([
        "def printer_method(*print_texts):",
        "    print('Hello')",
        "    print('code')",
        "    print('generation')",
        "    print('in')",
        "    print('pure')",
        "    print('Python')",
        "    print('!')",
    ])

    assert generated_code == expected


def test_generated_returns():
    @GeneratedFunction
    def generated_identity(
            generated_code_block: GeneratedCodeBlock,
            argument: any,
    ):
        with generated_code_block:
            return argument

    returned_value = generated_identity(42)
    assert returned_value == 42


def test_generated_modifies_arguments():
    @GeneratedFunction
    def generated_elementwise_incrementer(
            generated_code_block: GeneratedCodeBlock,
            lst: List[int],
    ):
        with generated_code_block:
            for i, element in enumerate(lst):
                lst[i] = element + 1

    lst = [4, 2]
    generated_elementwise_incrementer(lst)
    print(generated_elementwise_incrementer.get_source(lst))
    expected = [5, 3]
    assert lst == expected


def test_generated_propagates_exceptions():
    @GeneratedFunction
    def generated_raiser(
            generated_code_block: GeneratedCodeBlock,
    ):
        with generated_code_block:
            raise Exception

    with pytest.raises(Exception):
        generated_raiser()


def test_generated_is_not_closure():
    """
    Generated methods can only inline simple
    variables from the generator code,
    can't access or modify others.
    Cogpy won't help you implement fancier closures!
    """

    @GeneratedFunction
    def generated_not_closure_counter(
            generated_code_block: GeneratedCodeBlock,
    ):
        counter = count()
        with generated_code_block:
            return next(counter)

    with pytest.raises(NameError):
        generated_not_closure_counter()


def test_generated_passes_are_irrelevant():
    @GeneratedFunction
    def generated_counter_with_passes(
            generated_code_block: GeneratedCodeBlock,
    ):
        with generated_code_block:
            counter = 0
            for _ in range(10):
                counter += 1

            return counter

    assert generated_counter_with_passes() == 10


def test_mixing_generator_and_generated_variables_is_a_bad_idea():
    @GeneratedFunction
    def generated_with_mixed_variables(
            generated_code_block: GeneratedCodeBlock,
    ):
        var = 42
        with generated_code_block:
            var += 1
            return var

    with pytest.raises(SyntaxError):
        generated_with_mixed_variables()
