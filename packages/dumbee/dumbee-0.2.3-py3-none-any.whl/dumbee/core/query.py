class Query:
    """
    Database query

    Parameters
    ----------
    type : str
        one of 'exists', 'read', 'write', 'delete', or 'index'

    path : str
        resource path

    engine : dumbee.Engine
        the database engine

    content : any
        for 'write' queries, the content to save

    context : dict
        additional context data
    """

    def __init__(
        self, *, type: str, path: str, engine=None, content=None, context=None
    ):
        self.type = type
        self.path = path
        self.engine = engine
        self.content = content
        self.context = context or {}

    def replace(
        self, type=None, path=None, engine=None, content=None, context=None
    ) -> "Query":
        """
        Return a new query with modified attributes

        Parameters
        ----------
        type : str
            one of 'exists', 'read', 'write', 'delete', or 'index'

        path : str
            resource path

        engine : dumbee.Engine
            the database engine

        content : any
            for 'write' queries, the content to save

        context : dict
            additional context data

        Returns
        -------
        Query
        """
        return Query(
            type=type or self.type,
            path=path or self.path,
            engine=engine or self.engine,
            content=content or self.content,
            context=context or self.context,
        )
