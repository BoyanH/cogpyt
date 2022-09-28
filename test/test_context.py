import pytest
from cogpyt.context import GeneratedCodeBlock


@pytest.fixture
def generated_code_block():
    return GeneratedCodeBlock()


def test_generated_code_not_executed_on_generation(generated_code_block):
    prior_code_executed = True

    code_in_generated_block_executed = False
    with generated_code_block:
        code_in_generated_block_executed = True

    post_code_executed = True

    assert prior_code_executed
    assert not code_in_generated_block_executed
    assert post_code_executed


def test_generated_code_extraction(generated_code_block):
    with generated_code_block:
        print('some code')

    result = generated_code_block.export()
    expected = "print('some code')"

    assert result == expected


def test_generation_replaces_string_constants(generated_code_block):
    string = 'string'
    with generated_code_block:
        print(string)

    result = generated_code_block.export()
    expected = "print('string')"

    assert result == expected


def test_generation_replaces_numeric_constants(generated_code_block):
    number = 42.1337
    with generated_code_block:
        print(number)

    result = generated_code_block.export()
    expected = "print(42.1337)"

    assert result == expected


def test_generation_replaces_list_constants(generated_code_block):
    lst = [1, 3, 3, 7]
    with generated_code_block:
        print(lst)

    result = generated_code_block.export()
    expected = "print([1, 3, 3, 7])"

    assert result == expected


def test_generation_does_not_replace_instance_constants(generated_code_block):
    instance = object()
    with generated_code_block:
        print(instance)

    result = generated_code_block.export()
    expected = "print(instance)"

    assert result == expected


def test_generation_allows_multiple_blocks(generated_code_block):
    with generated_code_block:
        print('first line')

    with generated_code_block:
        print('second line')

    result = generated_code_block.export()
    expected = '\n'.join([
        "print('first line')",
        "print('second line')",
    ])

    assert result == expected


def test_generation_respects_indentation(generated_code_block):
    generated_code_block.indent()
    with generated_code_block:
        print('code')

    result = generated_code_block.export()
    expected = "    print('code')"

    assert result == expected


def test_generation_keeps_indentation(generated_code_block):
    generated_code_block.indent()
    with generated_code_block:
        print('first line')

    with generated_code_block:
        print('second line')

    result = generated_code_block.export()
    expected = '\n'.join([
        "    print('first line')",
        "    print('second line')",
    ])

    assert result == expected


def test_generation_allows_dedentation(generated_code_block):
    generated_code_block.indent()
    with generated_code_block:
        print('first line')

    generated_code_block.dedent()
    with generated_code_block:
        print('second line')

    result = generated_code_block.export()
    expected = '\n'.join([
        "    print('first line')",
        "print('second line')",
    ])

    assert result == expected


def test_generation_ignores_passes(generated_code_block):
    with generated_code_block:
        for i in range(42):
            pass

    generated_code_block.indent()
    with generated_code_block:
        print(i)

    result = generated_code_block.export()
    expected = '\n'.join([
        "for i in range(42):",
        "    pass",
        "    print(i)",
    ])

    assert result == expected


def test_mixing_generator_and_generated_variables_is_a_bad_idea(
        generated_code_block
):
    var = 42
    with generated_code_block:
        var += 1
        return var

    result = generated_code_block.export()
    expected = '\n'.join([
        '42 += 1',
        'return 42'
    ])

    assert result == expected
