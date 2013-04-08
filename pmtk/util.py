"""
Utility classes and functions
"""


class TitleMixin:
    """Mixin class for having a title that defaults to id"""

    def _getTitle(self):
        return self._title if self._title is not None else self.id

    def _setTitle(self, title):
        self._title = title

    title = property(_getTitle, _setTitle)
