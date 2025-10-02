class AuthServiceProvider:
    def register(self, app):
        print("🔑 AuthServiceProvider registered")

    def boot(self, app):
        print("🔐 AuthServiceProvider booted")
