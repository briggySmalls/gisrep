import outputs


def all_subclasses(cls):
    return cls.__subclasses__() + [g for s in cls.__subclasses__()
                                   for g in all_subclasses(s)]


class OutputManager(object):
    def __init__(self):
        subclasses = all_subclasses(outputs.AbstractOutput)
        self.output_forms = { cls.tag(): cls for cls in subclasses}

    def list(self):
        return keys(self.output_forms)

    def dump(self, tag, report):
        if tag in self.output_forms:
            self.output_forms[tag].dump(report)
        else:
            raise RuntimeError("Outputter not found")
