import json

from pydantic import TypeAdapter

MOCK_JSON_PATH = "app/tests/mock_"
JSON_EXTENSION = ".json"
ENCODING_UTF = "utf-8"


def open_mock_json(model_name: str, schema):
    with open(
        f"{MOCK_JSON_PATH}{model_name}{JSON_EXTENSION}", encoding=ENCODING_UTF
    ) as file:
        raw_data = json.load(file)

    adapter = TypeAdapter(list[schema])
    validated_objects = adapter.validate_python(raw_data)
    data_to_insert = [obj.model_dump(exclude={"id"}) for obj in validated_objects]

    return data_to_insert
