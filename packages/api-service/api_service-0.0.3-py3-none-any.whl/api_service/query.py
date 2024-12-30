from pydantic import BaseModel, ValidationError, create_model
from fastapi import HTTPException
import json
import urllib


def decode_query(query: str) -> dict:
    """
    Decodes a query string into a dictionary. If the query string is a URL-encoded JSON string,
    it decodes it as JSON; otherwise, it treats it as a standard query string.
    """
    # Split the query string into separate parameters
    params = query.split("&")
    decoded_result = {}

    for param in params:
        # URL-decode each parameter
        decoded_param = urllib.parse.unquote(param)

        # Check if the parameter is in JSON format
        try:
            # If it's JSON, load it and update the dictionary
            json_part = json.loads(decoded_param)
            if isinstance(json_part, dict):
                decoded_result.update(json_part)
        except json.JSONDecodeError:
            # If it's not JSON, process as a standard key-value pair
            key_value = decoded_param.split("=", 1)
            if len(key_value) == 2:
                key, value = key_value
                decoded_result[key] = value

    return decoded_result


def decode_and_validate_query(query: str, validation_model: BaseModel) -> dict:
    try:
        return validate_query_over_schema(
            validation_model=validation_model,
            query=decode_query(query),
        )

    except Exception as e:
        raise e


def validate_query_over_schema(validation_model: BaseModel, query: dict) -> dict:
    """Check if every field of the input query is contained in the validation_model.
    It will throw an HTTPException with status_code 422, with the details of the issue if incorrect.
    Otherwise it will return the validated query as a dictionary where the types match with the schema.
    """

    # Extract keys from both query and model
    base_fields = set(validation_model.__fields__)
    query_keys = set(query.keys())
    unique_fields = query_keys - base_fields

    # If the query has different keys -> status_code 422
    if unique_fields:
        raise HTTPException(
            status_code=422, detail=f"You can only use this keys {base_fields}"
        )

    query_mathing_fields = {
        field_name: (field.annotation, field.default)
        for field_name, field in validation_model.__fields__.items()
        if field_name in query_keys
    }

    model = create_model("QuerySubModel", **query_mathing_fields)

    # Try parsing the query in the newly created model to get full query validation

    try:
        validated_query = model(**query)
        return validated_query.dict()
    except ValidationError as e:
        raise HTTPException(
            status_code=422,
            detail=f"The type of your query don't match the schema. Details: {str(e)}",
        )
