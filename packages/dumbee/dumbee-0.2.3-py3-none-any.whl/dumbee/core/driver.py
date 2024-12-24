import abc
import easytree
import typing


class Driver(abc.ABC):
    """
    Abstract file system
    """

    def __init__(self, params: dict = None):
        self.params = easytree.dict(params or {})

    class DoesNotExist(Exception):
        """
        Resource does not exist exception
        """

        pass

    @abc.abstractmethod
    def exists(self, path: str) -> bool:
        """
        Return True if the node exists, False otherwise

        Parameters
        ----------
        path : str

        Returns
        -------
        bool
        """
        pass

    @abc.abstractmethod
    def index(self, path: str) -> typing.List[str]:
        """
        List the available children paths

        Parameters
        ----------
        path : str
            the file path

        Returns
        -------
        list[str]
        """
        pass

    @abc.abstractmethod
    def read(self, path: str) -> str:
        """
        Read the content of a node

        Parameters
        ----------
        path : str

        Returns
        -------
        str
        """
        pass

    @abc.abstractmethod
    def write(self, path: str, content: str) -> None:
        """
        Write content to a path

        Parameters
        ----------
        path : str
            the file path

        content : str
            the file content

        Returns
        -------
        None
        """
        pass

    @abc.abstractmethod
    def delete(self, path: str) -> None:
        """
        Delete a resource

        Parameters
        ----------
        path : str
            the file path

        Returns
        -------
        None
        """
        pass
