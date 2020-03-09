# -*- coding: utf-8 -*-
class Community(object):
    """A class representing a community."""

    def __init__(self, **kwargs):
        self.id = None
        self.title = None

        allowed_keys = {'id', 'title'}

        self.__dict__.update((k, v) for k, v in kwargs.items() if k in allowed_keys)

    def __repr__(self):
        return "Community(ID={id}, Title='{title}')".format(
            id=self.id,
            title=self.title
        )


class Street(object):
    """A class representing a street."""

    def __init__(self, **kwargs):
        self.id = None
        self.title = None

        allowed_keys = {'id', 'title'}

        self.__dict__.update((k, v) for k, v in kwargs.items() if k in allowed_keys)

    def __repr__(self):
        return "Street(ID={id}, Title='{title}')".format(
            id=self.id,
            title=self.title
        )


class WasteType(object):
    """A class representing a waste type."""

    def __init__(self, **kwargs):
        self.id = None
        self.title = None

        allowed_keys = {'id', 'title'}

        self.__dict__.update((k, v) for k, v in kwargs.items() if k in allowed_keys)

    def __repr__(self):
        return "WasteType(ID={id}, Title='{title}')".format(
            id=self.id,
            title=self.title
        )
