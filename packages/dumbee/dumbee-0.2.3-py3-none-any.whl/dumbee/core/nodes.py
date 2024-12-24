import abc
import uuid
import typing

if typing.TYPE_CHECKING:
    from .engine import Engine


class Node(abc.ABC):
    """
    Database node
    """

    def __init__(self, path: str, engine: "Engine"):
        self.path = path
        self.engine = engine

    @property
    def id(self) -> str:
        """
        Returns the id of the node

        Returns
        -------
        str
        """
        return self.path.rsplit("/", -1)[-1]

    def __repr__(self) -> str:
        """
        Returns the string representation

        Returns
        -------
        str
        """
        return f"<{type(self).__name__} path='{self.path}'/>"

    def __enter__(self):
        """
        Enter context manager

        Returns
        -------
        Node
        """
        return self

    def __exit__(self, *args, **kwargs):
        """
        Exit context manager
        """
        pass


class Record(Node):
    """
    Record interface

    Parameters
    ----------
    name : str, Path
        document name (excluding extension)

    collection : Collection
        parent collection
    """

    @property
    def collections(self) -> "Collections":
        """
        Returns a database under the current path
        """
        return Collections(path=self.path, engine=self.engine)

    def exists(self) -> bool:
        """
        Returns True if the document exists on disk.

        Returns
        -------
        bool
        """
        return self.engine.exists(self.path)

    def read(self) -> typing.Any:
        """
        Read the document

        Returns
        -------
        content : any
            the document content
        """
        return self.engine.read(self.path)

    def write(self, content: typing.Any) -> None:
        """
        Write the data

        Parameters
        ----------
        content : dict
            the document content

        Returns
        -------
        id : str
            the record id
        """
        self.engine.write(self.path, content=content)
        return self

    def delete(self) -> None:
        """
        Delete a document and any associated subcollection

        Returns
        -------
        None
        """
        self.engine.delete(self.path)


class Collection(Node):
    """
    Collection of documents
    """

    def __contains__(self, name: str) -> bool:
        """
        Returns True if a record of the given name exists
        in this collection

        Returns
        -------
        bool
        """
        return self.get(name).exists()

    def insert(self, id=None) -> Record:
        """
        Returns a Record

        Returns
        -------
        Record
        """
        return self.get(id or str(uuid.uuid4()))

    def get(self, name: str) -> Record:
        """
        Returns a Record for a given document name

        Parameters
        ----------
        name : str
            the document name (without any extension)
        """
        return Record(f"{self.path}/{name}", self.engine)

    def exists(self) -> bool:
        """
        Returns True if the collection exists in the database
        """
        return self.engine.exists(self.path)

    def all(self) -> typing.List[Record]:
        """
        Returns all the records under the current node

        Returns
        -------
        list[Record]
        """
        return [Record(path, self.engine) for path in self.engine.index(self.path)]

    def delete(self) -> None:
        """
        Delete collection and all records under the current node

        Returns
        -------
        None
        """
        self.engine.delete(self.path)


class Collections(Node):
    """
    Record set of children collections
    """

    def __getitem__(self, name) -> Collection:
        """
        Get a collection by name
        """
        return Collection(f"{self.path}/{name}", self.engine)

    def __contains__(self, name: str) -> bool:
        """
        Returns True if a collection of the given name
        exists in the collections
        """
        return self[name].exists()

    def all(self) -> typing.List[Collection]:
        """
        Returns all the collections under the current node

        Returns
        -------
        list[Collection]
        """
        return [Collection(path, self.engine) for path in self.engine.index(self.path)]

    def delete(self) -> None:
        """
        Delete set of collections (recursively)
        """
        self.engine.delete(self.path)
