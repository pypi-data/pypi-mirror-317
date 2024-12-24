import json
import dumbee


class Serializer(dumbee.Middleware):
    @property
    def paths(self) -> list:
        """
        Returns list of paths on which to execute this middleware

        Returns
        -------
        list
        """
        return self.params.get("paths", ["."])

    @property
    def encoder(self) -> json.JSONEncoder:
        """
        Return the JSON encoder
        """
        return self.params.get("serializer", json.JSONEncoder)

    @property
    def decoder(self) -> json.JSONDecoder:
        """
        Return the JSON decoder
        """
        return self.params.get("deserializer", json.JSONDecoder)

    def apply(self, query, next: callable):
        """
        Apply the middleware a query
        """
        return dumbee.Pipeline([self.encode, self.decode])(query, next)

    def encode(self, query, next: callable):
        """
        Serialize content
        """
        if query.type == "write":
            return next(
                query.replace(
                    content=json.dumps(
                        query.content,
                        indent=self.params.get("indent", 4),
                        cls=self.encoder,
                    )
                )
            )

        return next(query)

    def decode(self, query, next: callable):
        """
        Deserialize content
        """
        if query.type == "read":
            return json.loads(next(query), cls=self.decoder)
        return next(query)
