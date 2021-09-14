# test2doc
Generate documentation from tests.

To install:	```pip install test2doc```

# Motivation

If you're like me, you think that having tests and documentation is good, 
but writing them is soul-killing. 
It's repetitive and so easy to deviate from a consistent look, make mistakes, 
and all that jazz. 

Fortunately, there are tools out there to help out.
Tools that will transform your docs into tests, so you not only can 
make sure that the examples in your docs actually work, 
but also get some test coverage from your docs. 

That's `doc2test` stuff, and it's nice.

But what about `test2doc`?

What if you have a nicely commented test function like the following one in 
your `tests/` folder:

```python
def test_func(func, wrap):
    from inspect import signature

    # Just wrapping the func gives you a sort of copy of the func.
    wrapped_func = wrap(func)  # no transformations
    # The behavior remains the same:
    assert wrapped_func(2, 'co') == 'coco' == func(2, 'co')
    # ... and the signature as well:
    assert (
            str(signature(wrapped_func)) == "(a, b: str, c='hi')"
    )
```

Who's going to read that?

The nerds, okay, but not the normal people, the many users you'd have if 
you had this as a nicely formatted documentation. 

Something that would look like

## About `test_func(func, wrap)`

```python
from inspect import signature
```

Just wrapping the func gives you a sort of copy of the func.

```python
wrapped_func = wrap(func)  # no transformations
```

The behavior remains the same:

```python
assert wrapped_func(2, 'co') == 'coco' == func(2, 'co')
```

... and the signature as well:

```python
assert (
        str(signature(wrapped_func)) == "(a, b: str, c='hi')"
)

```

## You know what I'm getting at...

Do it like this:

```python
from test2doc import code_to_docs

docs = code_to_docs(test_func)
```

