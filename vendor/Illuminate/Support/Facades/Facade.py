class FacadeMeta(type):
    def __getattr__(cls, name):
        root = cls.get_facade_root()
        if root is None:
            raise AttributeError(f"Facade root for '{cls.__name__}' is not set")
        return getattr(root, name)

    def __call__(cls, *args, **kwargs):
        root = cls.get_facade_root()
        if root is None:
            raise AttributeError(f"Facade root for '{cls.__name__}' is not set")
        return root(*args, **kwargs)


class Facade(metaclass=FacadeMeta):
    _resolved = {}

    @classmethod
    def get_facade_accessor(cls):
        raise NotImplementedError("Facade must implement get_facade_accessor")

    @classmethod
    def get_facade_root(cls):
        accessor = cls.get_facade_accessor()
        return cls._resolved.get(accessor)

    @classmethod
    def swap(cls, instance):
        accessor = cls.get_facade_accessor()
        cls._resolved[accessor] = instance
