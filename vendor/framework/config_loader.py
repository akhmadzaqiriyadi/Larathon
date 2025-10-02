import os
import importlib.util

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONFIG_DIR = os.path.join(BASE_DIR, "config")

class Config:
    _cache = {}

    @classmethod
    def load(cls, name):
        if name in cls._cache:
            return cls._cache[name]

        file_path = os.path.join(CONFIG_DIR, f"{name}.py")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Config file not found: {name}.py")

        spec = importlib.util.spec_from_file_location(name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        cls._cache[name] = getattr(module, "config", {})
        return cls._cache[name]

    @classmethod
    def get(cls, key, default=None):
        """
        key: "app.name" atau "database.default"
        """
        parts = key.split(".")
        if len(parts) < 2:
            raise ValueError("Config key must be in 'file.key' format")

        file, subkey = parts[0], ".".join(parts[1:])
        config = cls.load(file)

        value = config
        for part in subkey.split("."):
            value = value.get(part) if isinstance(value, dict) else None
        return value if value is not None else default
