import functools
import abc
import easytree
import typing
import re


class Middleware(abc.ABC):
    """
    Abstract middleware class

    Parameters
    ----------
    params : dict
        middleware parameters, including:

            patterns : list
                list of paths to match

            exclusions : list
                list of paths to exclude from any matches

            handles : callable
                callback function to dynamically determine whether to handle a query
    """

    def __init__(self, params: dict = None):
        self.params = easytree.dict(params if params is not None else {})

    def __call__(self, query, next: callable):
        """
        Call the middleware
        """
        if not self.handles(query=query):
            return next(query)
        return self.apply(query=query, next=next)

    def handles(self, query) -> bool:
        """
        Determine whether the middleware should apply to the given query

        Returns
        -------
        bool
        """
        for pattern in self.params.get("exclusions", []):
            if re.match(pattern, query.path):
                return False

        for pattern in self.params.get("patterns", ["."]):
            if re.match(pattern, query.path):
                return True

        if callable(self.params.get("handles")):
            return self.params.handles(query)

        return False

    @abc.abstractmethod
    def apply(self, query, next: callable):
        raise NotImplementedError


class Pipeline(Middleware):
    """
    Sequence of middlewares

    Note
    ----
    Middlewares are called in ordered: the first in
    the pipeline will be called before the second, etc.
    """

    def __init__(self, middlewares: typing.List[Middleware], *, params=None):
        super().__init__(params=params)
        self.middlewares = middlewares

    def apply(self, query, next: callable):
        return self.wrap(next)(query)

    def wrap(self, func):
        """
        Wrap a function
        """
        return functools.reduce(
            lambda acc, func: lambda query: func(query, acc),
            reversed(self.middlewares),
            lambda query: func(query),
        )
