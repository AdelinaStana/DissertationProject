class AttributeModel:
    def __init__(self):
        self.type = "None"
        self.name = "None"
        self.calls = 0

    def set_type(self, type):
        self.type = type

    def set_name(self, name):
        self.name = name

    def add_call(self):
        self.calls += 1

    def set_calls(self, calls):
        self.calls = calls

    def get_type(self):
        return self.type

    def get_name(self):
        return self.name

    def get_calls(self):
        return self.calls