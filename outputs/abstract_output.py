from abc import ABCMeta, abstractmethod


class AbstractOutput(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def tag(self): pass

    @classmethod
    @abstractmethod
    def dump(self, report): pass
