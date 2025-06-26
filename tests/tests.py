from wrappity import Wrapper, inspect, unwrap, wrap

test_obj = {"a": 1, "b": [1, 2, 3], "c": {"d": 4}}
wrapped_obj = wrap(test_obj)


def test_wrap_unwrap():
    # test wrapping and unwrapping
    assert isinstance(wrapped_obj, Wrapper)
    unwrapped_obj = unwrap(wrapped_obj)
    assert test_obj == unwrapped_obj


def test_inspect():
    # test inspecting
    paths = inspect(wrapped_obj)
    assert paths == ["a=1", "b[0]=1", "b[1]=2", "b[2]=3", "c.d=4"]


def test_underscore_access():
    # test underscore access
    assert wrapped_obj.a._ == 1
    assert wrapped_obj.b[1]._ == 2
    assert wrapped_obj.c.d._ == 4


def test_access_miss():
    # test access miss
    assert bool(wrapped_obj.e) is False
    assert wrapped_obj.e._ is None


def test_missed_access_hook():
    # test missed access hook
    missed_called_with = {}

    def missed_access_callable(object_, what, access_type):
        missed_called_with["object_"] = object_
        missed_called_with["what"] = what
        missed_called_with["access_type"] = access_type

    wrapped_obj_hooked = wrap(test_obj, missed_access_hook=missed_access_callable)
    wrapped_obj_hooked.e
    assert missed_called_with["what"] == "e"
    assert missed_called_with["access_type"] == Wrapper.ACCESS_TYPE_DICT
    assert unwrap(missed_called_with["object_"]) == test_obj


def test_inspect_show_values_true():
    # test inspecting with show_values=True
    paths = inspect(wrapped_obj, show_values=True)
    assert paths == ["a=1", "b[0]=1", "b[1]=2", "b[2]=3", "c.d=4"]


def test_inspect_show_values_false():
    # test inspecting with show_values=False
    paths = inspect(wrapped_obj, show_values=False)
    assert paths == ["a", "b[0]", "b[1]", "b[2]", "c.d"]


def test_ensure_list_on_none():
    # test _ensure_list on None
    assert wrapped_obj.e._el()._ == []


def test_ensure_list_on_existing_list():
    # test _ensure_list on existing list returns the same list
    wrapped_obj.b._el()
    assert isinstance(wrapped_obj.b._, list)
    assert wrapped_obj.b._ == [1, 2, 3]


def test_underscore_unwraps_nested_structure():
    # test underscore unwraps nested structure
    assert type(wrapped_obj.c._["d"]) is int
    assert wrapped_obj.c._["d"] == 4


def test_attr_translations():
    # test attribute translations
    test_obj_translate = {"a-b": 1}
    wrapped_obj_translate = wrap(test_obj_translate, attr_translations={"ab": "a-b"})
    assert wrapped_obj_translate._ab._ == 1


def test_ensure_list_on_value():
    # test _ensure_list on a value
    wrapped_val = wrap(5)
    wrapped_val._el()
    assert wrapped_val._ == [5]


def test_missed_access_hook_list():
    # test missed access hook for list
    missed = False

    def missed_access_callable(object_, what, access_type):
        nonlocal missed
        missed = True
        assert what == 5
        assert access_type == Wrapper.ACCESS_TYPE_LIST

    wrapped_obj_hooked = wrap(test_obj, missed_access_hook=missed_access_callable)
    wrapped_obj_hooked.b[5]
    assert missed


def test_bool_behavior():
    # test __bool__ behavior
    assert bool(wrap(None)) is False
    assert bool(wrap([])) is False
    assert bool(wrap({})) is False
    assert bool(wrap(0)) is False  # Wraps the number, so the wrapper itself is not None
    assert bool(wrap([1])) is True


def test_iteration():
    # test __iter__
    assert [i._ for i in wrapped_obj.b] == [1, 2, 3]
    assert list(wrapped_obj.c.items())[0][0] == "d"


def test_len():
    # test __len__
    assert len(wrapped_obj.b) == 3
    assert len(wrapped_obj.c) == 1
    assert len(wrap(None)) == 0


def test_dict_methods():
    # test dict methods
    assert list(wrapped_obj.c.keys()) == ["d"]
    assert list(wrapped_obj.c.values())[0]._ == 4
    assert list(wrapped_obj.c.items())[0][0] == "d"


def test_repr_str():
    # test __repr__ and __str__
    assert "wrapped" in repr(wrapped_obj)
    assert str(wrapped_obj.a) == "1"
    assert str(wrapped_obj.e) == ""


def test_tuple_wrapping():
    # test tuple wrapping
    test_tuple = (1, 2, {"a": 3})
    wrapped_tuple = wrap(test_tuple)
    assert isinstance(wrapped_tuple._, list)
    assert wrapped_tuple[2].a._ == 3


def test_unwrap_non_wrapper():
    # test unwrap on non-wrapper
    assert unwrap(123) == 123
    assert unwrap("hello") == "hello"


def test_inspect_show_types_true():
    # test inspecting with show_types=True
    paths = inspect(wrapped_obj, show_types=True)
    assert paths == [
        "a=1 (<class 'int'>)",
        "b[0]=1 (<class 'int'>)",
        "b[1]=2 (<class 'int'>)",
        "b[2]=3 (<class 'int'>)",
        "c.d=4 (<class 'int'>)",
    ]


def test_inspect_filter_by_regex():
    # test inspecting with filter_by regex
    paths = inspect(wrapped_obj, filter_by=r"b\[\d\]")
    assert paths == ["b[0]=1", "b[1]=2", "b[2]=3"]


def test_inspect_show_types_and_filter_by():
    # test inspecting with show_types=True and filter_by regex
    paths = inspect(wrapped_obj, show_types=True, filter_by=r"b\[\d\]")
    assert paths == [
        "b[0]=1 (<class 'int'>)",
        "b[1]=2 (<class 'int'>)",
        "b[2]=3 (<class 'int'>)",
    ]