# Wrappity Usage Guide

This guide provides a comprehensive overview of the Wrappity library, its features, and how to use them effectively.

## Wrapping and Unwrapping

The core functionality of Wrappity revolves around the `wrap()` and `unwrap()` functions.

-   `wrap(object)`: Takes a Python object (typically a dictionary or a list) and returns a `Wrapper` object. This process is recursive, meaning all nested dictionaries and lists within the object are also wrapped.
-   `unwrap(wrapped_object)`: Takes a `Wrapper` object and returns the original, unwrapped object.

**Example:**

```python
from wrappity import wrap, unwrap

my_dict = {'a': {'b': [1, 2]}}
wrapped = wrap(my_dict)

print(wrapped)
# Output: wrapped(<class 'dict'>): {'a': wrapped(<class 'dict'>): {'b': wrapped(<class 'list'>): [wrapped(<class 'int'>): 1, wrapped(<class 'int'>): 2]}}

unwrapped = unwrap(wrapped)
print(unwrapped)
# Output: {'a': {'b': [1, 2]}}

assert my_dict == unwrapped
```

## The Wrapper object and getting the actual wrapped value

When you wrap an object, you get a `Wrapper` instance. To access the underlying value at any point in the chain, you use the special `_` attribute.

**Example:**

```python
from wrappity import wrap

wrapped = wrap({'a': {'b': 5}})

# Accessing the wrapped values
print(wrapped.a._)
# Output: {'b': wrapped(<class 'int'>): 5}

print(wrapped.a.b._)
# Output: 5
```

If you try to access an attribute that doesn't exist, Wrappity won't raise an error. Instead, it will return a `Wrapper` object around `None`.

```python
print(wrapped.x.y.z._)
# Output: None
```

This allows for safe and concise access to nested data without the need for multiple `if` checks.

## Ensuring lists

A common use case is to iterate over a list that may or may not exist in the data. The `_el()` method (short for "ensure list") helps with this. If the wrapped object is not a list, `_el()` will turn it into one.

-   If the wrapped value is `None`, it becomes an empty list `[]`.
-   If the wrapped value is not a list (e.g., a number or a string), it becomes a list containing that single value.
-   If the wrapped value is already a list, it remains unchanged.

**Example:**

```python
from wrappity import wrap

wrapped = wrap({'a': 1, 'b': [1, 2]})

# On a non-list value
print(wrapped.a._el()._)
# Output: [1]

# On an existing list
print(wrapped.b._el()._)
# Output: [1, 2]

# On a non-existent key
print(wrapped.c._el()._)
# Output: []
```

## How to handle Python-incompatible attributes

Sometimes, dictionary keys may contain characters that are not valid in Python identifiers (e.g., hyphens, spaces). Wrappity provides a mechanism to handle this through attribute translations.

You can pass an `attr_translations` dictionary to the `wrap()` function. This dictionary maps a valid Python attribute name to the actual key in the dictionary.

**Example:**

```python
from wrappity import wrap

data = {'user-id': 123, 'user-name': 'test'}
wrapped = wrap(data, attr_translations={'user_id': 'user-id', 'user_name': 'user-name'})

print(wrapped.user_id._)
# Output: 123

print(wrapped.user_name._)
# Output: 'test'
```

## Access misses - getting to know

Wrappity can be configured to notify you when an attempt is made to access a non-existent key or index. This is done by providing a `missed_access_hook` function to `wrap()`.

The hook function will be called with three arguments:

-   `object_`: The `Wrapper` object on which the access was missed.
-   `what`: The key or index that was accessed.
-   `access_type`: The type of access, either `Wrapper.ACCESS_TYPE_DICT` or `Wrapper.ACCESS_TYPE_LIST`.

**Example:**

```python
from wrappity import wrap, Wrapper

missed_accesses = []

def my_hook(object_, what, access_type):
    missed_accesses.append((what, access_type))

data = {'a': [1, 2]}
wrapped = wrap(data, missed_access_hook=my_hook)

# Trigger the hook
wrapped.b
wrapped.a[5]

print(missed_accesses)
# Output: [('b', 'access_type_dict'), (5, 'access_type_list')]
```

## Inspecting Wrapped Objects

The `inspect()` function is a powerful tool for debugging and understanding the structure of your wrapped objects. It returns a list of all possible paths to the leaf nodes in the data.

`inspect()` has several useful parameters:

-   `show_values` (bool, default `True`): Whether to include the values of the leaf nodes in the output.
-   `show_types` (bool, default `False`): Whether to show the data type of the leaf values.
-   `filter_by` (str, default `None`): A regular expression to filter the paths.

**Example:**

```python
from wrappity import wrap, inspect

data = {'a': 1, 'b': [1, 2, 3], 'c': {'d': 4}}
wrapped = wrap(data)

# Default inspect
print(inspect(wrapped))
# Output: ['a=1', 'b[0]=1', 'b[1]=2', 'b[2]=3', 'c.d=4']

# Without values
print(inspect(wrapped, show_values=False))
# Output: ['a', 'b[0]', 'b[1]', 'b[2]', 'c.d']

# With types
print(inspect(wrapped, show_types=True))
# Output: ['a=1 (<class 'int'>)', 'b[0]=1 (<class 'int'>)', 'b[1]=2 (<class 'int'>)', 'b[2]=3 (<class 'int'>)', 'c.d=4 (<class 'int'>)']

# Filtering
print(inspect(wrapped, filter_by=r'b\[\d\]'))
# Output: ['b[0]=1', 'b[1]=2', 'b[2]=3']
```