# Option Builder
from option.option import Option


class OptionBuilder:
    def __init__(self):
        self.name = ""
        self.description = ""
        self.type = None
        self.default = None

    def set_name(self, name):
        self.name = name
        return self

    def set_description(self, description):
        self.description = description
        return self

    def set_type(self, type):
        self.type = type
        return self

    def set_default(self, default):
        self.default = default
        return self

    def build(self):
        return Option(self.name, self.description, self.type, self.default)
