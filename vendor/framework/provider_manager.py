import importlib

class ProviderManager:
    def __init__(self, providers):
        self.providers = providers
        self.instances = []

    def boot(self, app):
        for provider in self.providers:
            module_path, class_name = provider.rsplit(".", 1)
            module = importlib.import_module(module_path)
            cls = getattr(module, class_name)
            instance = cls()
            if hasattr(instance, "register"):
                instance.register(app)
            if hasattr(instance, "boot"):
                instance.boot(app)
            self.instances.append(instance)
