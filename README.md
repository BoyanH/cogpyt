# Cogpyt -- Code Generation in (pure) Python


## Getting Started


**Installation** - Cogpyt is available on PyPI

```shell
$ pip install cogpyt
```

**Usage**
```pycon
>>> import cogpyt
>>> @cogpyt.GeneratedFunction
... def generated_printer(
...         generated_code_block: cogpyt.GeneratedCodeBlock,
...         amount: int,
... ):
...     for i in range(amount):
...         with generated_code_block:
...             print(i)
...
```

When calling `generated_printer`, cogpyt will first combine the code from
all `with generated_code_block` contexts and then execute it.

```pycon
>>> generated_printer(5)
0
1
2
3
4
```

For debugging purposes, you can also examine the generated Python code.

```pycon
>>> print(generated_printer.get_source(3))
def generated_printer(amount):
    print(0)
    print(1)
    print(2)
```

Notice how the counter `i` from the generator scope was inlined in the generated code.
This only works for built-in types. Also notice that the generator argument `amount`
was left as an argument in the generated function. This is indeed the case for
all arguments, so they can be freely used in generated code. 
Cogpyt does not yet perform any sort of pruning. Even `pass` statements, required
for example to generate just the header of an if statement, are left intact, since
they are just syntactic sugar and thus irrelevant in execution time.

**Disclaimer**: This is a proof of concept implementation. As such, it might fail in
completely unexpected ways. As a great Pythonista once said
> This is probably not something 
> that you're gonna take back to work and start applying unless you want to get fired. 

**Another Disclaimer**: Cogpyt only works when the source is stored in a file. 
This also explains why the example notebooks don't define any cogpyt-powered functions
but import them instead. It would be technically possible to lift this
constraint, but this is out-of-scope for this project, at least initially.

## But Why Tho?

I was recently on a vacation in Greece, where I am certain I was once again able
to experience a true spiritual awakening. As advised, I was really 
listening to my inner voice, primarily drinking a lot of Ouzo, reading and diving. 
The last exercise proved crucial not to lose that pesky inner voice.
What I was reading turns out to be the motivation behind this project, but in
a rather odd way. Beautiful Code, edited by Andy Oram and Greg Wilson, is composed of
thirty-three chapters, each giving a leading computer scientist's
take on the most beautiful code they ever encountered.
A chapter about on-the-fly code generation, written by no other than Charles Petzold,
that same Petzold who made Turing's great work accessible to an average
Joe like me, is the reason why you are now reading my awakened thoughts.
The author once again didn't disappoint and was able to present a
great idea in a very understandable manner. But the idea is not what moved me
the most. I have readily seen a healthy dose of such trickery throughout my computer
science education. I have also written a fair amount of low level code and that, that
was the last straw that led me to write this project, as well as the necessary rant that follows.

WHY? Why are computer scientists so, for the lack of a better word, elitist?
Why are we so protective of our work? Can I generate some code in C#? Sure, you
just need to write some intermediate language. It's easy, just like assembly,
you just need to learn the new syntax and opcodes. You know assembly, right?
No? Are you ... incompetent?!?

A line of assembly a day keeps the boss at bay, amirite? 
Sure, when implementing an operating system, sooner or later, 
some assembly will come into play. But so will a context switch need to be
implemented, at which point one quickly understands how expensive this process
is, especially when virtual memory is involved. Then why do we voluntarily keep
doing this to ourselves? While the current regular expression character matches the current
text character, **increment the pointers** and proceed recursively.
If the element of the image processing kernel is -1, emit **OpCodes.Neg** 
(wait, what was on the **stack** again?). WAT? These stick out like a sore thumb, don't they?
In the software these examples are taken from, this is a jump from the highest level of
abstraction to the lowest, just between two source code lines!
I am not convinced this is the only possible way to write efficient code.

In first semester I took a course where our homeworks were mostly to
implement simple algorithms in assembly. I would come home from
work and start awakening my spirits while implementing the given algorithm
in a high level language. Once I had tested the implementation
and was sufficiently awakened, I would proceed with the awakening
and simultaneously translate the code, line by line, in assembly. 
It always worked! And I was, even extremely awakened, hardly an expert!
I believe a true computer scientist should be busy designing the
most optimal solution, in any convenient formal language, and that bringing
this result in a more efficient format is a process we should 
be capable of automating. When it comes to purely translational
processes, as during my first-semester awakening sessions,
there are readily great tools at hand such as 
[Numba](https://numba.pydata.org/). The goal of this project
is to handle situations where on-the-fly code generation 
might come handy, in a manner accessible to any programmer,
without enforcing that apparently so beloved context switch.
It does not attempt to achieve this in an end-to-end manner,
but rather to be used in conjunction with other available solutions.
And it's just a proof of concept!

## The General Example

See [2d-convolution.pdf](examples/2d-convolution.pdf)

## License

[MIT](LICENSE)
