from .driver import Driver
from .middlewaring import Pipeline
from .nodes import Collections
from .query import Query


class Engine:
    """
    Root database engine
    """

    def __init__(self, *, driver: Driver, middlewares: Pipeline):
        self.driver = driver
        self.middlewares = middlewares

    def handle(self, query: Query):
        """
        Handle a query
        """

        def handle(query: Query):
            if query.type == "exists":
                return self.driver.exists(query.path)

            if query.type == "read":
                return self.driver.read(query.path)

            if query.type == "touch":
                return self.driver.touch(query.path)

            if query.type == "write":
                return self.driver.write(query.path, query.content)

            if query.type == "delete":
                return self.driver.delete(query.path)

            if query.type == "index":
                return self.driver.index(query.path)

            raise ValueError(f"Unexpected query type '{query.type}'")

        return self.middlewares.wrap(handle)(query.replace(engine=self))

    def exists(self, path: str):
        return self.handle(Query(type="exists", path=path))

    def read(self, path: str):
        return self.handle(Query(type="read", path=path))

    def write(self, path: str, content):
        return self.handle(Query(type="write", path=path, content=content))

    def delete(self, path: str):
        return self.handle(Query(type="delete", path=path))

    def index(self, path: str):
        return self.handle(Query(type="index", path=path))

    @property
    def collections(self) -> Collections:
        """
        Returns the root-level collections
        """
        return Collections(".", self)
