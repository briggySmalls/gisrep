"""
Helper classes for allowing location of classes by type
"""


def get_subclasses(parent):
    """Gets the subclasses of the provided class, recursively

    Args:
        parent (type): Class to find subclasses of

    Returns:
        list: Subclasses

    """
    return parent.__subclasses__() + [g for s in parent.__subclasses__()
                                      for g in get_subclasses(s)]


class Locator(object):
    """Class that finds descendents of Locatable class

    Attributes:
        lookup (dict): Mapping between parent class and its children
    """

    def __init__(self, locatable_class):
        self.lookup = {cls.tag: cls for cls in get_subclasses(locatable_class)}

    def locate(self, tag=None):
        """Locates the descendent(s) of the locatable class

        Args:
            tag (None, optional): Tag for class to lookup

        Returns:
            list: All locatable classes if tag argument is not supplied.
                  Otherwise returns the locatable with the specified tag or
                  None if no matching class is found

        Raises:
            RuntimeError: Description
        """
        try:
            return self.lookup.values() if tag is None else self.lookup[tag]
        except KeyError as exc:
            raise RuntimeError("Tag not found") from exc

    def list(self):
        """Gets the tags of all locatable classes

        Returns:
            list: Collection of all locatable class tags
        """
        return self.lookup.keys()


class Locatable(object):  # pylint: disable=too-few-public-methods
    """Class that can be found by Locator
    """

    @property
    def tag(self):
        """Returns the tag for the Locatable class

        Raises:
            NotImplementedError: Description
        """
        raise NotImplementedError(
            "tag attribute must be defined on Locatable class")
