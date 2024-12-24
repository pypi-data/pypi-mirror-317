class PropState:
    yes_options: list[str] = ["y", "yes", "enable", "enabled", "on", "true", "t"]
    no_options: list[str] = ["n", "no", "disable", "disabled", "off", "false", "f"]
    options: list[str] = yes_options + no_options
    def __init__(self, state: "bool | PropState"):
        self.state: bool = state if isinstance(state, bool) else state.state # NOQA
    @classmethod
    def from_string(cls, string: str):
        if string.lower() in cls.yes_options:
            return cls(True)
        elif string.lower() in cls.no_options:
            return cls(False)
        else:
            raise KeyError(f"{string} does not fit <{'|'.join(cls.options)}>")
    def to_string(self):
        return "enabled" if self.state else "disabled"
    def __bool__(self):
        return self.state