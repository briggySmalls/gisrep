import outputs


def all_subclasses(cls):
    return cls.__subclasses__() + [g for s in cls.__subclasses__()
                                   for g in all_subclasses(s)]


class OutputManager(object):
    def __init__(self):
        self.subclasses = all_subclasses(outputs.AbstractOutput)

    def list(self):
        return [cls.tag() for cls in self.subclasses]

    def dump(self, tag, report):
        for cls in self.subclasses:
            if cls.tag() == tag:
                cls.dump(report)
                break
