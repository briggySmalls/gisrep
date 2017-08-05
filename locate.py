from abc import ABCMeta, abstractmethod


def get_subclasses(cls):
    return cls.__subclasses__() + [g for s in cls.__subclasses__()
                                   for g in get_subclasses(s)]

class Locator(object, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, locatable_class):
        self.lookup = {cls.tag: cls for cls in get_subclasses(locatable_class)}

    def locate(self, tag=None):
        try:
            return self.lookup.values() if tag is None else self.lookup[tag]
        except KeyError as exc:
            raise RuntimeError("Tag not found") from exc
            

    def list(self):
        return self.lookup.keys()


class Locatable(object, metaclass=ABCMeta):
    @property
    def tag(self):
        raise NotImplementedError("tag attribute must be defined on Locatable class")
