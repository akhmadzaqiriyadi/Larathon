class App:
    _bindings = {}

    @classmethod
    def bind(cls, key, instance):
        cls._bindings[key] = instance

    @classmethod
    def make(cls, key):
        return cls._bindings[key]
