import os
import pathlib
import dumbee
import shutil
import re
import typing
import filelock


class Filesystem(dumbee.Driver):
    """
    File-based filesystem

    Parameters
    -----------
    root : pathlib.Path
        the path to the root directory

    extensions : list[tuple[str, str]]
        list of (path pattern, file extensions) tuples
    """

    class Node:
        """
        Filesystem node

        Parameters
        ----------
        root : pathlib.Path
            the database root path

        path : pathlib.Path
            the filename relative to the root (including any extension)
        """

        def __init__(self, root: pathlib.Path, path: pathlib.Path):
            self.root = root
            self.path = path

        @property
        def filename(self) -> pathlib.Path:
            """
            Returns the full filename
            """
            return pathlib.Path(self.root, self.path)

        @property
        def dirname(self) -> pathlib.Path:
            """
            Returns the full dirname
            """
            return pathlib.Path(self.root, self.name)

        @property
        def name(self) -> str:
            """
            Returns the node name (without any extension)
            """
            return os.path.splitext(self.path)[0]

        @property
        def extension(self):
            """
            Returns the node extension (if any)
            """
            return os.path.splitext(self.path)[1]

        def exists(self) -> bool:
            """
            Returns True if the node exists on the filesystem
            """
            return os.path.exists(self.filename) or os.path.exists(self.dirname)

        def __enter__(self):
            """
            Returns self
            """
            return self

        def __exit__(self, *args, **kwargs):
            """
            Convenience context-manager
            """
            pass

    def __init__(self, root: pathlib.Path, *, extensions: list = None):
        self.root = pathlib.Path(root).absolute()
        self.extensions = extensions or [(".", "txt")]

    def resolve(self, path: str) -> Node:
        """
        Convert a resource path to a Node

        Parameters
        ----------
        path : str
            the resource path

        Returns
        -------
        Node
        """
        if path == ".":
            return Filesystem.Node(self.root, "")

        for pattern, extension in self.extensions:
            if re.match(pattern, path):
                return Filesystem.Node(self.root, f"{path}.{extension}")
        raise ValueError(f"Unable to resolve '{path}' to a filename")

    def exists(self, path: str) -> bool:
        """
        Return True if a node exists at the given path, False otherwise

        Parameters
        ----------
        path : str
            the resource path

        Returns
        -------
        bool
        """
        with self.resolve(path) as node:
            return os.path.exists(node.filename) or os.path.exists(node.dirname)

    def read(self, path: str) -> str:
        """
        Read the content of a node at a given path

        Parameters
        ----------
        path : str
            the resource path

        Returns
        -------
        str
        """
        with self.resolve(path) as node:
            if os.path.exists(node.filename):
                with open(node.filename, mode="r") as file:
                    return file.read()

            # node exists but with no associated content
            if os.path.exists(node.dirname):
                return None

        raise dumbee.core.Driver.DoesNotExist(f"Database entry '{path}' does not exist")

    def write(self, path: str, content: str) -> None:
        """
        Write node's content at a given path

        Parameters
        ----------
        path : str
            the resource path

        content : str
            the file content

        Returns
        -------
        None
        """
        with self.resolve(path) as node:
            if not os.path.exists(node.filename.parent):
                os.makedirs(node.filename.parent)

        with filelock.FileLock(f"{node.filename}.lock"):
            with open(node.filename, mode="w") as file:
                file.write(content)

    def delete(self, path: str) -> None:
        """
        Delete node (both content and nested collections)

        Parameters
        ----------
        path : pathlib.Path
            the resource path

        Returns
        -------
        None
        """
        with self.resolve(path) as node:
            if os.path.exists(node.filename):
                os.remove(node.filename)

            if os.path.exists(node.dirname):
                shutil.rmtree(node.dirname)

    def index(self, path: str) -> typing.List[pathlib.Path]:
        """
        List children nodes at given path

        Returns
        -------
        list[pathlib.Path]
        """
        with self.resolve(path) as node:
            if not os.path.exists(node.dirname):
                return []

            return sorted(
                set(
                    self.resolve(f"{node.name}/{os.path.splitext(name)[0]}").name
                    for name in os.listdir(node.dirname)
                )
            )
