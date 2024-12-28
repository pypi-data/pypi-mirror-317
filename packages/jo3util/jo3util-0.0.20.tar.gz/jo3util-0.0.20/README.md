# README

A bunch of functionality in here, but the main one is `store.load_or_create`.
It might get its own package someday, when it's less before-pre-alpha-sneakpeak-demo as it's now.

## load_or_create

The main idea is that an object's storage path should be inferable from the arguments with which it was created.
In reality we often keep track of an object and its path seperately, which can work out poorly.
The `load_or_create` function bundles an object's creation, load, save and path function together such that anyone working with the code less often has to think about storage locations and more often can focus on the functionality of their code.

### the status quo

A common pattern has you write the following 4 functions for objects that are expensive to create:

```python
from pathlib import Path
import pickle  # We use pickle as an example here.

def create_obj(name, some_kwarg=1):
    """This function takes long, so we don't want to run it redundantly."""
    return obj

def save_obj(obj, path):
    """Instead we write a save function..."""
    with open(path, "wb") as file:
        pickle.dump(obj, file)

def load_obj(path):
    """...and a load function so we only need to create the object once."""
    with open(path, "rb") as file:
        return pickle.load(file)

def infer_path(name):
    """We need to keep track where the created object is stored."""
    return "./obj/" + str(name) + ".pkl"

# When you have the above 4 fuctions, this pattern will start to occur.
name = "MyObject"
path = infer_path(name)
if Path(path).exists():
    obj = load_obj(load)
else:
    obj = create_obj(name, some_kwarg=0)
    save_obj(obj, path)
```

In some cases, you want to create and save many variations of the object.
It might be better to hash its characteristics and use that as part of the path.

```python
import sha256
import json

def infer_path(name, **some_other_kwargs):
    hash = str(sha256(json.dumps(some_other_kwargs)).hexdigest())
    return "./obj/" + hash + ".pkl"
```

### the problem

The above is fine and dandy, but when someone wants to use your obj,
they'd need to keep track of your 4 separate functions.

You can dress it up as such:
```python
def get_obj(name, some_kwarg):
    path = infer_path(name)
    if path.exists():
        obj = load_obj(load)
    else:
        obj = create_obj(name, some_kwarg=some_kwarg)
        save_obj(obj, path)
    return obj
```
But that takes a lot of freedom away from your user, who might have their
own ideas on where and how the object should be loaded or stored.

### the solution

```python
from jo3util.store import load_or_create
get_obj = load_or_create(
    load=load_obj,
    save=save_obj,
    path_fn=infer_path,
)(create_obj)

obj = get_obj(name, some_kwarg=0)

# We can now infer the path of an object from its creation arguments.
path = get_obj.path(name, some_kwarg=0)

# We also can use `get_obj.path_of_obj` to recall the path of any object 
# that `get_obj` returned in he past.
assert path == get_obj.path_of_obj(obj)
```

You can now elegantly pack the four functions together.
But you still have the flexibility to alter the path function on the fly:

```python
get_obj.path_fn = lambda hash: f"./{hash}.pkl"
```

Now, storing different objects of which one is dependent on the other, becomes intuitive and elegant:

```python
# This code is written at the library level

get_human = load_or_create(
    path_fn=lambda name: "./" + name + "/body.pkl"
    # If you omit the save and load functions, load_or_create will use pickle.
)(lambda name: name)

get_finger_print = load_or_create(
    path_fn=lambda human, finger: get_human.dir_from_obj(human) / f"{finger}.print"
)(lambda human, finger: f"{human}'s finger the {finger}")

# This code is what a user can work with.

assert not get_human.path("john").exists()  # ./john/body.pkl
human = get_human("john")
assert get_human.path("john").exists()

finger_print = get_finger_print(human, "thumb")
assert get_finger_print.path(human, "thumb") == "./john/thumb.print"
```

The finger print is now always stored in the same directory as where the human's `body.pkl` is stored.
You don't need to keep track of the location of `body.pkl`.

### four functions in one

The main trick is to match the parameter names of the `create` function (in our case `create_obj`)
with those of the three other subfunctions (in our case `load_obj`, `save_obj` and `infer_path`).

The three subfunctions's allowed parameters are mostly a non-strict superset of the create function's
parameters.

When you call the `load_or_create`-wrapped `get_obj`, something like this happens:

```python
def call_fn_with_filtered_arguments(fn, *args, **kwargs):
    """ call `fn` with only the subset of `args` and `kwargs` that it expects.

    This is necessary, as python will complain if a function receives any
    argument for which there is no function parameter.
    So 
    def fn(a):
        pass
    fn(a=0, b=1)
    will error, so we need to remove b before calling fn.

    This example function is wrong, if you're curious you need to check the
    source code.
    """
    # Get the names of the paremeters that `fn` accepts.
    path_parameters = get_parameters_that_fn_expects(fn)
    # Filter for positinoal arguments that `fn` accepts.
    args = [a for i, a in enumerate(args) if name_of_positional(i, fn) in path_parameters]
    # Filter for keyword arguments that `fn` accepts.
    kwargs = {k: a for k, a in kwargs.items() if k in path_parameters}
    # Call `fn` with the filtered subset of the original args and kwargs.
    return fn(*args, **kwargs)

def get_obj_pseudo_code(*args, **kwargs):
    hash = some_hash_fn(*args, **kwargs)
    path = call_fn_with_filtered_arguments(infer_path, *args, hash=hash, **kwargs)
    if path.exists():
        return call_fn_with_filtered_arguments(
            load_obj,
            *args,
            path=path,
            file=open(path, "rb"),
            **kwargs
        )

    obj = create_obj(*args, **kwargs)
    call_fn_with_filtered_arguments(
        save_obj,
        qbj,
        *args,
        path=path,
        file=open(path, "wb"),
        **kwargs
    )
    return obj
```

So, the load, save and path functions you provide do not have to have the same signature as the create
function does, but you can call them _as if_ they are the create function.

### philosophy

The main idea is that some object's storage location should be inferrable from the arguments 
during its creation call.

In reality, we tend to separately keep track of some object's path, its arguments and itself.
This tends to go bad when we need to load, save or create the object in some other context.
It becomes easy to forget where some object ought to be stored. 
Or it can happen that different places where the same object is handled, have different opinions on its storage location.

It can lead to duplicates; forgetting where the object was stored; or losing a folder of data
because the folder is too unwieldy to salvage.

By packaging a function with its load and save countparts and a default storage location, we don't
need to worry about the storage location anymore and can focus on creating and using our objects.

If we ever do change our minds on the ideal storage location, then there is an obvious central place
for changing it, and that change then easily immediately applies to _all_ the places where
that object's path needs to be determined.
