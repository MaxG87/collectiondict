# collectiondict - Create multidicts more easily

This package simplifies the creation of multimappings from various sources. It
provides the functions `collectiondict`, `reverse_mapping` and
`reverse_multimapping`. In all three cases the return value will be of type
`dict[_ValueT, Collection[_KeyT]]`.

All three functions expect the target collection to be provided as an argument.
The supported collections are fixed. Only the built-in collections `Counter`,
`frozenset`, `list`, `set`, and `tuple` as well as their subclasses are
supported. If a unsupported collection is passed, an exception is raised.
However, `mypy` will warn about it.

Due to the limits of Pythons type annotations, it is not possible to specify
the correct return type for the custom classes. Thus, custom classes are
supported but the return type is inferred to be the parent class (e.g. `set`),
as opposed to be the class passed in (e.g. `class MySet(set)`).

In order to have the best type inference, it is recommended to **cast** `clct_t`
to specify the value type. Passing a specialised collection class is **not**
supported currently. The examples show how to use a cast.
