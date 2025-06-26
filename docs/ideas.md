# Suggested Features and Improvements for Wrappity

## 1. Default Values for Missed Access
Currently, accessing a non-existent key or index returns a `Wrapper` around `None`. It would be very useful to allow the user to specify a default value to be returned in these cases. This could be implemented as an argument to the access method, for example: `wrapped.get('non_existent_key', 'my_default_value')`.

## 2. In-place Modification
The library is currently read-only. A major feature would be to allow in-place modification of the wrapped data structure. This would mean implementing `__setattr__` and `__delattr__` on the `Wrapper` class, so you could do things like:
```python
wrapped.a.b.c = "new value"
del wrapped.a.b[0]
```

## 3. Rich Comparisons
The `Wrapper` class could implement rich comparison operators like `__eq__`, `__ne__`, etc. This would allow for more intuitive comparisons between `Wrapper` objects, where the comparison would be performed on the underlying wrapped values. For example:
```python
# Instead of this:
unwrap(wrapped_obj1) == unwrap(wrapped_obj2)

# You could do this:
wrapped_obj1 == wrapped_obj2
```

## 4. Expanded `inspect()` Functionality - ✅ implemented
The `inspect()` function is great for debugging. It could be made even more powerful by adding:
*   **Filtering**: Allow the user to filter the paths based on a regular expression or a filter function.
*   **Value Types**: Add an option to show the data type of the leaf values.

## 5. Comprehensive Testing - ✅ implemented
I noticed that the `tests/tests.py` file is currently empty. Building a comprehensive test suite using a framework like `pytest` would be the most critical improvement. It would ensure the library's reliability, prevent regressions, and give you more confidence when adding new features.

## 6. Complete the Documentation - ✅ implemented
The `docs/guide.md` file has a good structure, but the sections are empty. Filling these sections with detailed explanations and code examples for each feature would be very helpful for new users. A "Quickstart" guide in the `README.md` would also be a great addition.
