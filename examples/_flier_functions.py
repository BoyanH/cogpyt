import cogpyt


@cogpyt.GeneratedFunction
def generated_printer(
        generated_code_block: cogpyt.GeneratedCodeBlock,
        amount: int,
):
    for i in range(amount):
        with generated_code_block:
            print(i)
