"""
Helper classes for allowing location of classes by type
"""

from abc import ABCMeta, abstractmethod


def get_subclasses(cls):
    """
    Gets the subclasses (recursive)
    
    :param      cls:  The class to find descendents of
    :type       cls:  type
    
    :returns:   The subclasses.
    :rtype:     list
    """
    return cls.__subclasses__() + [g for s in cls.__subclasses__()
                                   for g in get_subclasses(s)]

class Locator(object, metaclass=ABCMeta):
    """
    Class that finds descendents of Locatable class
    """

    @abstractmethod
    def __init__(self, locatable_class):
        self.lookup = {cls.tag: cls for cls in get_subclasses(locatable_class)}

    def locate(self, tag=None):
        """
        Locates the descendent(s) of the locatable class
        
        :type       self:  Locator
        :type       tag:   type
        
        :returns:   All locatable classes if tag argument is not supplied.
                    Otherwise returns the locatable with the specified tag or
                    None if no matching class is found
        :rtype:     list or type or None
        """
        try:
            return self.lookup.values() if tag is None else self.lookup[tag]
        except KeyError as exc:
            raise RuntimeError("Tag not found") from exc

    def list(self):
        """
        Gets the tags of all locatable classes
        
        :returns:   Collection of all locatable class tags
        :rtype:     list
        """
        return self.lookup.keys()


class Locatable(object, metaclass=ABCMeta):
    """
    Class that can be found by Locator
    """

    @property
    def tag(self):
        """
        Returns the tag for the Locatable class
        
        :returns:   The tag of the class
        :rtype:     string
        """
        raise NotImplementedError("tag attribute must be defined on Locatable class")
