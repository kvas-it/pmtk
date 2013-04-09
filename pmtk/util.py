"""
Utility classes and functions
"""


class TitleMixin:
    """Mixin class for having a title that defaults to id and a description"""

    description = ''

    def __getTitle(self):
        return self.__title if self.__title is not None else self.id

    def __setTitle(self, title):
        self.__title = title

    title = property(__getTitle, __setTitle)
