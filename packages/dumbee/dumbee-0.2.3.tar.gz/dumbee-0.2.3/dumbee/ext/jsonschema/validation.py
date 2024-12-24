import jsonschema
import jsonschema.protocols
import dumbee


def defaultize(
    validator: jsonschema.protocols.Validator,
) -> jsonschema.protocols.Validator:
    """
    Set defaults defined in the schema

    If the default is a callable, call such function passing the
    property name and the instance

    Returns
    -------
    Validator
    """
    validate_properties = validator.VALIDATORS["properties"]

    def set_defaults(validator, properties, instance, schema):
        for property, subschema in properties.items():
            if "default" in subschema:
                if callable(subschema["default"]):
                    instance.setdefault(
                        property, subschema["default"](property, instance)
                    )
                else:
                    instance.setdefault(property, subschema["default"])

        for error in validate_properties(
            validator,
            properties,
            instance,
            schema,
        ):
            yield error

    return jsonschema.validators.extend(
        validator,
        {"properties": set_defaults},
    )


class Validator(dumbee.Middleware):
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
    def validator(self):
        return self.params.get("validator", defaultize(jsonschema.Draft202012Validator))

    @property
    def schema(self):
        return self.params.get("schema", {"type": "object"})

    def validate(self, data):
        self.validator(self.schema).validate(data)
        return data

    def apply(self, query, next):
        if query.type == "read":
            return self.validate(next(query))

        if query.type == "write":
            return next(query.replace(content=self.validate(query.content)))

        return next(query)
