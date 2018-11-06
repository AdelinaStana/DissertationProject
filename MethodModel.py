class MethodModel:
    def __init__(self):
        self.type = "None"
        self.name = "None"
        self.args = []
        self.locals = []

    def set_type(self, type):
        self.type = type

    def set_name(self, name):
        self.name = name

    def add_locals(self, local):
        self.locals.append(local)

    def add_call(self, local_name):
        for local in self.locals:
            if local.get_name() == local_name:
                local.add_call()

    def add_args(self, arg):
        self.args.append(arg)

    def get_args(self):
        return self.args

    def get_locals(self):
        return self.locals

    def get_name(self):
        return self.name

    def get_type(self):
        return self.type
