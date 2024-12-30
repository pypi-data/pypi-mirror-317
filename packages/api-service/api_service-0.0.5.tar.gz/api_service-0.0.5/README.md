# Description of the Encryption Module

This module provides essential functionalities for secure authentication and password management in Python applications, particularly useful in web services developed with FastAPI. It is designed with a focus on security, efficiency, and ease of use.

## Features

### JWT Token Management

- `create_jwt_token(payload: dict)`: Creates a JWT (JSON Web Token) with a custom payload, typically including user details like ID and role. The token is encrypted using a secret key and an algorithm specified in the environment variables. It has a default expiration of 7 days.
- `check_token(token: str)`: Validates the given JWT token, verifying its integrity and authenticity. Returns `True` if the token is valid, otherwise `False`.
- `read_token_from_header(request: Request)`: Extracts and validates a JWT token from the HTTP request header. If the token is invalid or expired, it raises an `HTTPException` with appropriate status codes.
- `read_token(token: str)`: Validates a given string token. Raises an `HTTPException` if the token is invalid or expired, otherwise, returns the token's payload.

### Password Encryption and Verification

- `encrypt_password(password: str)`: Encrypts a plain password using bcrypt, providing a secure way to store passwords.
- `check_password(plain_password: str, hashed_password: str)`: Verifies a plain password against its hashed version, typically used during the login process.

This module is particularly suitable for web applications requiring robust authentication mechanisms and secure password handling.

# Description of the Query Module

This module is designed to handle and validate query strings in Python applications, especially in the context of web APIs developed using FastAPI and Pydantic. It focuses on flexibility and reliability in processing and validating query strings.

## Features

### Query String Decoding

- `decode_query(query: str)`: Decodes a query string into a dictionary. It can handle both URL-encoded JSON strings and standard query strings. For JSON strings, it parses them into a dictionary, and for standard query strings, it processes them as key-value pairs.

### Query Validation

- `decode_and_validate_query(query: str, validation_model: BaseModel)`: Decodes the given query string and then validates it against a specified Pydantic model. It ensures that the query matches the expected schema and data types.
- `validate_query_over_schema(validation_model: BaseModel, query: dict)`: Validates a dictionary (typically the result of a decoded query) against a Pydantic model. It checks if all fields in the query are contained in the model and match the expected types. If the query is incorrect, it raises an `HTTPException` with details of the discrepancy.
