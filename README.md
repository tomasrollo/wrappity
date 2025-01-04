# Wrappity

_Wrappity is a Python package for easier access to deeply nested dictionaries._

_Pure Python, no dependencies, lightweight (200 LOC)._

## What does it do

Wrappity allows you to access deeply nested dictionaries and combinations of `dicts` and `lists` using simple attribute 'dot' notation.
It is especially useful when your input are volatile json structures where you can't enforce uniformity.

Instead of...
```python
value = my_dict['foo'][3]['bar'][5]['baz']['this_is_what_I_want']
```

...you can write
```python
import wrappity
wrapped_dict = wrappity.wrap(my_dict)
value = wrapped_dict.foo[3].bar[5].baz.this_is_what_I_want._
```

**Why bother?**

Because if you want to properly account for errors, you might end up with something like:
```python
if 'foo' in my_dict \
	and len(my_dict['foo']) >= 3 \
	and 'bar' in my_dict['foo'][3] \
	and len(my_dict['foo'][3]['bar']) >= 5 \
	and 'baz' in my_dict['foo'][3]['bar'][5]:
	value = my_dict['foo'][3]['bar'][5]['baz'].get('this_is_what_I_want','my default value')
```

With Wrappity you don't need to explicitely care about all the elements in the path to be there or not (or have enough items), if anything is missing on the way, Wrappity just gives you `None` at the end.

This allows (more elegant) constructs like this:
```python
value = wrapped_dict.foo[3].bar[5].baz.this_is_what_I_want._ or "my default value"
print(value)
'my default value' # in case any of the foo, bar or baz are not there
```

To learn more about why Wrappity was created and what use cases it's good for see [here](docs/why.md).

## Installation

_coming soon_

## Usage

There are 3 key functions in Wrappity:
1. `wrap()` - takes an object and wraps it for easy access
2. `unwrap()` - reverse function - give it a wrapped object and it gives you the original back
2. `inspect()` - for introspection - gives you a list of all paths to all leaves in your object incl. their values

### Wrap

### Unwrap

### Inspect

## Where can I learn more?

See [Wrappity Guide](docs/guide.md).

## Why is it called Wrappity?

Because you do _wrappity wrap_ and that's it! 😉

## License

Licensed under the
[MIT](https://github.com/tomasrollo/wrappity/blob/main/LICENSE) License.

