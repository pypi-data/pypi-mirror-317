from hashlib import sha256
import inspect
import io
import json
from pathlib import Path
import pickle
from typing import Tuple

from .hollow import HollowObject


def with_filtered_args(fn):
    """
    Return a version of the input function that ignores instead of errors on
    unknown arguments.
    """
    arg_filter = {param.name for param in inspect.signature(fn).parameters.values()
                  if param.kind == param.POSITIONAL_OR_KEYWORD 
                  or param.kind == param.KEYWORD_ONLY}

    def inner(*args, **kwargs):
        # Filter any keyword arguments not present in small_fn.
        kwargs = {k: v for k, v in kwargs.items() if k in arg_filter}
        return fn(*args, **kwargs)

    return inner, arg_filter


class HashingWriter(io.BytesIO):
    def __init__(self):
        super().__init__()  # Initialize the BytesIO buffer
        self.hash = sha256()  # Initialize the SHA-256 hash object

    def write(self, b):
        self.hash.update(b)  # Update the hash with the data being written
        return 0
        # return super().write(b)  # Write the data to the BytesIO buffer

    def writelines(self, lines):
        for line in lines:
            self.write(line)

    def get_hash(self):
        return self.hash.hexdigest()  # Return the hexadecimal digest of the hash


class LoadOrCreateCFG:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class load_or_create:

    def __init__(
        self,
        load=pickle.load,
        save=pickle.dump,
        path_fn=lambda hash: hash + ".pkl",
        hash_len=8,
        save_args=False,
        save_json=False,
        plain_text=False,
        path=None,
    ):
        self.load=with_filtered_args(load)[0]
        self.load_arg_names = {p.name for p in inspect.signature(load).parameters.values()}
        self.save=with_filtered_args(save)[0]
        self.save_arg_names = {p.name for p in inspect.signature(save).parameters.values()}
        self.path_fn=path if path is not None else path_fn
        self.hash_len=hash_len
        self.save_args=save_args
        self.save_json=save_json
        self.plain_text=plain_text
        self.obj_to_args = {}

        # To be initialied by Loc.
        self.fn = lambda x: x
        self.arg_names = []

    def __call__(self, fn):
        return Loc(self, fn)

    def args_to_kwargs(self, args, kwargs, **extra):
        return extra | kwargs | {self.arg_names[i]: a for i, a in enumerate(args)}

    def load_wrapper(self, **load_args):
        """
        load_wrapper returns None or an abject.
        Iff it returns None, the object is deemed not-loaded and thus,
        self.fn needs to be called to create the object.
        It can return None, because self.load returns None or if self.load
        expects an open file, but no such file exists.
        """
        # Check whether self.load does not expect an open file.
        if "file" in load_args or "file" not in self.load_arg_names:
            return self.load(**load_args)

        path = load_args["path"]
        # If self.load expects an open file but there is none, run self.fn.
        if not path.exists():
            return None

        with open(path, "r" if self.plain_text else "rb") as file:
            # If specified, the first line is a json of the keyword arguments.
            if self.save_args:
                file.readline()
            return self.load(**{"file": file} | load_args)


    def save_wrapper(self, obj, *args, **kwargs):
        """Only open a file if the save function requests you to.
        """
        merged_args = self.args_to_kwargs(args, kwargs)

        path = Path(merged_args["path"])
        path.parent.mkdir(parents=True, exist_ok=True)

        if "file" not in self.save_arg_names:
            return self.save(obj, **merged_args)

        if "file" in merged_args:
            file = merged_args["file"]
        else:
            file = open(path, "w" if self.plain_text else "wb")

        if self.save_args:
            file.write(self.to_json(**kwargs))

        self.save(obj, **{"file": file} | merged_args)

        if "file" not in merged_args:
            file.close()


    def to_json(self, **kwargs) -> bytes:
        """Serialize all keyword arguments to json. 
        We never serialize positional arguments"""
        return (
            json.dumps(
                kwargs,
                default=lambda x: vars(x) if hasattr(x, "__dict__") else str(x)
            ) + "\n"
        ).encode("utf-8")

    def prime(self, *args, **kwargs):
        """Make sure some object is on disk, but don't load or return it."""
        path = self.path(*args, **kwargs)
        if path.exists(): return

        obj = self.fn(*args, **kwargs)
        if obj is None: return

        self.save_wrapper(obj, *args, **{"path": path} | kwargs)
        if "file" in self.save_arg_names: self.hash_obj({"path": path} | kwargs)
        if self.save_json:
            path.with_suffix(".kwargs.json").write_bytes(self.to_json(**kwargs))

    # Functions to do with hashing keyword arguments and determining an
    # object's path from its arguments.

    def hash_kwargs(self, **kwargs):
        """Serialize all keyword arguments to json and hash it."""
        json_args = self.to_json(**kwargs)
        hash_str = sha256(json_args, usedforsecurity=False).hexdigest()
        return hash_str[:self.hash_len]

    def path_and_hash(self, *args, **kwargs) -> Tuple[Path, str]:
        path_fn, arg_filter = with_filtered_args(self.path_fn)

        hash = self.hash_kwargs(
            # Do not have arguments in the hash that path_fn uses.
            **{k: a for k, a in kwargs.items() if k not in arg_filter}
        )

        path_args = self.args_to_kwargs(args, kwargs, hash=hash)

        path = Path(path_fn(**path_args))

        return path, hash

    def hash(self, *args, **kwargs) -> str:
        """Hash the keyword arguments.
        Note that the hash is dependent on the path function of this instance:
        All arguments of the path function are excluded from the hash."""
        return self.path_and_hash(*args, **kwargs)[1]

    def path(self, *args, **kwargs) -> Path:
        return self.path_and_hash(*args, **kwargs)[0]

    def dir(self, *args, **kwargs) -> Path:
        return self.path(*args, **kwargs).parent

    # Functions to do with inferring an object's arguments by keeping track of
    # its hash.

    def hash_obj(self, kwargs):
        """After saving or loading the object, we get its hash from the
        storage file.
        This hash we can later use, to infer the arguments that created this
        object.
        """
        path = Path(kwargs["path"])
        if not path.exists():
            return
        with open(path, "rb") as file:
            if self.save_args:
                file.readline()
            hash = sha256(file.read()).hexdigest()
        self.obj_to_args[hash] = kwargs

    def args_from_obj(self, obj, *args, **kwargs):
        """Hash the object using the user-provided self.save.
        Then retrieve its arguments by looking up hashes of previously loaded
        or saved objects.
        Also ssee self.hash_obj
        """
        if id(obj) in self.obj_to_args:
            return self.obj_to_args[id(obj)]
        file = HashingWriter()
        self.save(obj, **self.args_to_kwargs(args, kwargs), file=file)
        hash = file.get_hash()
        return self.obj_to_args[hash]

    def path_from_obj(self, obj, *args, **kwargs):
        # If the object passed is a HollowObject, we can infer the args without
        # calling it.
        if hasattr(obj, "_get_call"):
            _, args, kwargs = obj._get_call()
            return self.path(*args, **kwargs)
        return self.args_from_obj(obj, *args, **kwargs)["path"]

    def dir_from_obj(self, obj, *args, **kwargs):
        return self.path_from_obj(obj, *args, **kwargs).parent

    def cfg(self, *args, **kwargs):
        """If you don't care about some object, but only about it's path,
        but you still need to pass an object to some other function in order
        to get it's path, you can pass a LoadOrCreateCFG instead, saving you
        from loading or creating that object..
        """
        return HollowObject(lambda x: x, *args, **kwargs)


class Loc(load_or_create):
    def __init__(self, parent, fn):
        self.__dict__.update(parent.__dict__)
        self.fn = fn
        self.arg_names = [p.name for p in inspect.signature(fn).parameters.values()]

    def __call__(self, *args, **kwargs):
        # Store the keyword arguments into json and hash it to get the storage path.
        path = self.path(*args, **kwargs)
        merged_args = self.args_to_kwargs(args, kwargs, path=path)

        obj = self.load_wrapper(**merged_args)
        if obj is not None: 
            self.obj_to_args[id(obj)] = {"path": path} | kwargs
            if "file" in self.save_arg_names:
                self.hash_obj({"path": path} | kwargs)
            return obj

        obj = self.fn(*args, **kwargs)
        if obj is None: return obj

        self.save_wrapper(obj, *args, **{"path": path} | kwargs)
        self.obj_to_args[id(obj)] = {"path": path} | kwargs
        if "file" in self.save_arg_names:self.hash_obj({"path": path} | kwargs)
        if self.save_json:
            path.with_suffix(".kwargs.json").write_bytes(self.to_json(**kwargs))

        return obj


