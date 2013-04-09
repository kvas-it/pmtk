"""
Utility classes and functions
"""


class TitleMixin:
    """Mixin class for having a title that defaults to id and a description"""

    description = ''
    __properties = {}

    def __getTitle(self):
        return self.__title if self.__title is not None else self.id

    def __setTitle(self, title):
        self.__title = title

    title = property(__getTitle, __setTitle)

    def setProperty(self, id, value):
        self.setProperties(**{id: value})

    def setProperties(self, **kw):
        """Set custom properties on this object."""
        if self.__properties == {}:
            self.__properties = dict(kw)
        else:
            self.__properties.update(kw)

    def getProperty(self, id, default=None):
        """Return property value or None."""
        return self.__properties.get(id, default)
