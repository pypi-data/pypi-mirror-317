# FastAPI Bearer Authorization

A robust bearer token authentication and authorization middleware for FastAPI applications.

> [!WARNING]  
> This project is in early development and may not be suitable for production use.

## Features

- Easy-to-use bearer token authentication
- Fine-grained permission-based authorization using unique operation IDs
- HTTP Verb based authorization, using the `HTTP_VERB:<VERB_NAME>` format
- Configurable via environment variables or direct configuration
- Secure token generation and validation

## Installation

```bash
uv add fastapi-bearer-authzn
```

## Quick Start

```python
from fastapi import FastAPI, Depends
from fastapi_bearer_authzn import BearerAuthDependency

# Initialize the auth dependency, with the config coming from an environment variable
auth = BearerAuthDependency(from_env=True)

app = FastAPI()

@app.get("/protected")
def protected_route(user_id: str = Depends(auth)):
    return {"message": "Access granted", "user_id": user_id}
```

## Configuration

Generate a configuration file using the included CLI:

```bash
# Run the bootstrap command for environment configuration
uvx fastapi-bearer-authzn bootstrap_config -o env -n 1

FASTAPI_BEARER_AUTHZN_CONFIG='{"224848fe-45df-4173-bc8c-535442611311":{"hashed_token":"ec274bd79a868d17884897455fbbb29c65f3ca076a58c3de8b2121f407a5184518013c7b38cebbffe00c4aabfa03d3dbbbc5df1ddbd206aa94936930c14e3706","user_identifier":"user_a3e7a662-764d-4afe-b84d-98bc10efccbe@example.com","permissions":["*"]}}'

Generated tokens:
224848fe-45df-4173-bc8c-535442611311: fastapi_bearer_authzn_224848fe-45df-4173-bc8c-535442611311_JZy73nSZdvtLYIO1C0o1Rv3dyemqpEeG0eGE_AIqwxs
```

## Usage

1. Initialize the `BearerAuthDependency` with your configuration.
2. Use the dependency in your FastAPI route decorators.
3. The middleware will handle authentication and authorization based on the operation IDs and HTTP verbs.

## Operation ID-based and HTTP Verb-based Authorization

This module uses FastAPI's operation IDs and HTTP verbs for fine-grained authorization. By default, FastAPI generates an operation ID for each route, which can be inspected in the OpenAPI JSON schema. You can also override these with custom operation IDs.

Given this FastAPI app:

```python
@app.get("/resource1")
def get_resource_1(user_id: str = Depends(auth)):
    # Uses FastAPI's default operation ID, obtain it from the OpenAPI JSON schema, and use it in the config
    return {"message": "Access to resource 1 granted"}

@app.post("/resource2", operation_id="create_resource_2")
def create_resource_2(user_id: str = Depends(auth)):
    # Even better: Use a custom operation ID, then simply reference "create_resource_2" in the config to grant access to this route
    return {"message": "Resource 2 created"}
```

An exemplary config may look as follows:

```jsonc
{
  "e2403b7b-822b-4a0c-8586-85adb672169c": {
    "hashed_token": "e725c175f719caae1dcc0f0421663402c90f551790f869fcef786fb217a8084e20dfbef7ac47309926919a659da9db4f0cb1062dec578bc907bc18991bbb390f",
    "user_identifier": "Used by microservice X", # arbitrary string, for you to identify the user/service
    "permissions": [
      "HTTP_VERB:GET",
      "create_resource_2"
    ]
  }
}
```

This config grants access to all paths via `GET` and only to the `create_resource_2` path via `POST`.

## Testing

Run the tests using `pytest`:

```bash
# Test latest supported Python version
uv run pytest tests -vv

# Test all supported Python versions
for py in 3.8 3.9 3.10 3.11 3.12 3.13; do
    uv run --python $py pytest tests -vv 
done
```

## License

This project is licensed under the MIT License.

## Publish to PyPI

For the time being, you can publish the package to pypi manually.

```bash
uv build
uvx twine check dist/* # ensure that the distribution’s long description will render correctly on PyPI
uvx twine upload dist/* --skip-existing  # or `uvx twine upload --repository testpypi dist/* --skip-existing` for testpypi
```

You will be prompted for a PyPI API token.
