import pytest
import dumbee


@pytest.fixture
def conn(tmp_path):
    return dumbee.Engine(
        driver=dumbee.drivers.Filesystem(tmp_path, extensions=[(".", "json")]),
        middlewares=dumbee.Pipeline(
            [
                dumbee.ext.logging.Logger(),
                dumbee.ext.jsonschema.Validator(
                    {
                        "schema": {
                            "type": "object",
                            "properties": {"name": {"type": "string"}},
                        }
                    }
                ),
                dumbee.ext.json.Serializer(),
            ]
        ),
    )


def test_1(conn):
    conn.collections["users"].get("me").write({"message": "Hello world"})
    assert conn.collections["users"].get("me").exists()
    assert conn.collections["users"].exists()


def test_2(conn):
    conn.collections["users"].get("me").write({"message": "Hello world"})
    conn.collections["users"].delete()
    assert conn.collections["users"].exists() is False


def test_query_id(conn):
    with conn.collections["users"].insert() as record:
        assert isinstance(record.id, str)
