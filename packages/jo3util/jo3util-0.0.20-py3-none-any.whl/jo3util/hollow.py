from typing import TypeVar, Generic, Callable, Type, Union

T = TypeVar("T")


def HollowObject(init_fn: Union[T, Callable[..., T]], *args, **kwargs) -> T:
    """ Return an object that only gets initialized when any of its attributes are accessed.

    :param init_fn: Function that initializes the real object.
    :param args: Positional arguments for the init_fn.
    :param kwargs: Keyword arguments for the init_fn.
    """

    # Case for types.
    if isinstance(init_fn, type):
        base_class = init_fn
    # Case for functions.
    elif hasattr(init_fn, "__annotations__") and "return" in init_fn.__annotations__:
        base_class = init_fn.__annotations__["return"]
    # Case for callable class instances.
    elif hasattr(init_fn.__call__, "__annotations__") and "return" in init_fn.__call__.__annotations__:
        base_class = init_fn.__call__.__annotations__["return"]
    # Case for unnannotated non-type callables.
    else:
        base_class = object

    def initialize(hollow_object):
        real_obj = init_fn(*args, **kwargs)

        try:
            # Change the type of `self` to match the real object
            hollow_object.__class__ = real_obj.__class__
            hollow_object.__dict__ = real_obj.__dict__  # Copy the real object's attributes
            return False

        # For certain builtin immutable types, we can't change the __class__ or __dict__.
        # This means the instance will always stay a HollowObject subclass and the below
        # wrapper will keep firing for all calls.
        except TypeError:
            hollow_object._real_obj = real_obj
            return True

    def wrap(fn):
        def inner(self, *args, **kwargs):
            if hasattr(self, "_real_obj") or initialize(self):
                return object.__getattribute__(self._real_obj, fn.__name__)(*args, **kwargs)
            else:
                return object.__getattribute__(self, fn.__name__)(*args, **kwargs)
        return inner

    class HollowObject(base_class):

        def __init__(self):
            pass

        def __getattribute__(self, name):
            # Avoid infinite recursions.
            if name in ["__dict__", "__class__", "_real_obj", "_get_call"]:
                return super().__getattribute__(name)

            if hasattr(self, "_real_obj") or initialize(self):
                return getattr(self._real_obj, name)
            else:
                return getattr(self, name)

        def __setattr__(self, name, value):
            # Avoid infinite recursions.
            if name in ["__dict__", "__class__", "_real_obj", "_get_call"]:
                return super().__setattr__(name, value)

            if hasattr(self, "_real_obj") or initialize(self):
                setattr(self._real_obj, name, value)
            else:
                setattr(self, name, value)

        @staticmethod
        def _get_call():
            return init_fn, args, kwargs

        @wrap
        def __str__(self):
            return ""

        @wrap
        def __repr__(self):
            return ""

        @wrap
        def __add__(self, _):
            pass

        @wrap
        def __iter__(self, _):
            pass

        # todo: add all the magic functions

    return HollowObject()


def lazy(fn):
    """ Replace fn with a lazy function.

    A lazy function does not immediately fire, but instead returns an object
    that contains the function call. If anything of the object is accessed,
    it is created in-place and the accessed thing is returned."""
    def lazy_(*args, **kwargs):
        return HollowObject(fn, *args, **kwargs)
    return lazy_


if __name__ == "__main__":

    # Example usage of an object with type hints
    class FullObject:
        def __init__(self, value: int):
            self.value = value
            print("initialized")

        def __str__(self):
            return f"Value is {self.value}"

    hollow = HollowObject(FullObject, value=42)
    print(type(hollow))
    # Linters will know that `hollow` behaves like `FullObject`.
    #
    # Only now does hollow get initialized.
    print(hollow)
    # The type of hollow is now FullObject, so no future calls will be made through the wrapper.

    # Example usage of the lazy decorator.

    print("\nstarting string tests")

    @lazy
    def lazy_greeting(name) -> str:
        print("preparing to greet")
        return "hello " + name

    message = lazy_greeting("john")
    print(type(message))
    print([char for char in message])
    # because message is a subclass of str, we can't change the class's type.
    # this means that all future calls on it, will be through the wrapper
    # and message stays an HollowObject type.

