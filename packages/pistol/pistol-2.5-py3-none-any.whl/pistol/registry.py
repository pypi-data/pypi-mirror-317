class CommandRegistry:
    def __init__(self):
        self.commands = {}
    def register(self, name: str, handler):
        self.commands[name] = handler
    def execute(self, name, *args, **kwargs):
        self.commands[name](*args, **kwargs)