# dumbee

Pretend it's a database

## Installation

```
pip install dumbee
```

## Getting started

```python
import dumbee

# create an Engine
db = dumbee.Engine(
    driver=dumbee.drivers.Filesystem("./data", extensions=[(".", "json")]),
    middlewares=dumbee.Pipeline(
        [
            dumbee.ext.logging.Logger(),
            dumbee.ext.jsonschema.Validator(
                {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string"
                            },
                            "age":{
                                "type":"number"
                            }
                        },
                        "required":["name"]
                    },
                    "paths":[
                        "./users/[A-Za-z]+$"
                    ]
                }
            ),
            dumbee.ext.json.Serializer(),
        ]
    ),
)

# write and read back a record
me = (
    db
    .collections["users"]
    .get("me")
    .write({"name":"David", "age":32})
    .read()
)

# nested collection
repos = (
    db
    .collections["users"]
    .get("me")
    .collections["repositories"]
    .get("OSS")
    .write(["easychart","easytree","doubledate","dumbee"])
    .read()
)
```
