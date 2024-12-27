from secrets import token_urlsafe
from typing import Any
from uuid import uuid4

from fastapi import APIRouter, Depends, FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.testclient import TestClient
from typing_extensions import Dict

from fastapi_bearer_authzn import BearerAuthDependency, bootstrap_config, HTTP_VERB_PREFIX


def create_app():
    config, tokens = bootstrap_config(no_identities=4)
    second_user = config[list(config.keys())[1]]
    second_user["permissions"] = ["get_protected_resource_v1_protected_resource_get"]
    third_user = config[list(config.keys())[2]]
    third_user["permissions"] = ["unknown_operation_id"]
    fourth_user = config[list(config.keys())[3]]
    fourth_user["permissions"] = [f"{HTTP_VERB_PREFIX}GET"]
    dep = BearerAuthDependency(config=config)
    router = APIRouter(prefix="/v1")

    @router.get(
        path="/unprotected-resource",
        description="Get an unprotected resource",
        response_model=Any,
        tags=["Demo Routes"],
    )
    def get_unprotected_resource() -> Dict[str, bool]:
        return {"success": True}

    @router.get(
        path="/protected-resource",
        description="Get a protected resource",
        response_model=Any,
        tags=["Demo Routes"],
        dependencies=[Depends(dep)],
    )
    def get_protected_resource() -> Dict[str, bool]:
        return {"success": True}

    @router.post(
        path="/protected-resource",
        description="Create a protected resource",
        response_model=Any,
        tags=["Demo Routes"],
        dependencies=[Depends(dep)],
    )
    def create_protected_resource() -> Dict[str, bool]:
        return {"created": True}

    app = FastAPI()
    app.include_router(router)
    return app, config, tokens


# Create a TestClient with the FastAPI app
app, config, tokens = create_app()
client = TestClient(app)
openapi_spec = get_openapi(
    title=app.title,
    version=app.version,
    openapi_version=app.openapi_version,
    description=app.description,
    routes=app.routes,
)


# Helper function to generate a valid Authorization header
def generate_auth_header(bearer_id: str) -> Dict[str, str]:
    api_key = tokens[bearer_id]["token"]
    return {"Authorization": f"Bearer {api_key}"}


def test_unprotected_resource():
    response = client.get("/v1/unprotected-resource")
    assert response.status_code == 200
    assert response.json() == {"success": True}


def test_protected_resource_no_auth():
    response = client.get("/v1/protected-resource")
    assert response.status_code == 403


def test_protected_resource_with_valid_auth():
    # Use one of the valid bearer IDs from the config
    valid_bearer_id = next(iter(config.keys()))
    auth_header = generate_auth_header(valid_bearer_id)

    response = client.get("/v1/protected-resource", headers=auth_header)
    assert response.status_code == 200
    assert response.json() == {"success": True}


def test_protected_resource_with_invalid_auth():
    invalid_bearer_id = str(uuid4())
    invalid_secret = token_urlsafe(32)
    api_key = f"fastapi_bearer_authzn_{invalid_bearer_id}_{invalid_secret}"

    response = client.get(
        "/v1/protected-resource", headers={"Authorization": f"Bearer {api_key}"}
    )
    assert response.status_code == 403


def test_protected_resource_with_specific_permission():
    # Get the bearer ID for the second user (with specific permission)
    specific_perm_bearer_id = list(config.keys())[1]
    auth_header = generate_auth_header(specific_perm_bearer_id)

    response = client.get("/v1/protected-resource", headers=auth_header)
    assert response.status_code == 200
    assert response.json() == {"success": True}


def test_protected_resource_with_unknown_operation_id():
    # Get the bearer ID for the third user (with unknown operation ID)
    unknown_op_bearer_id = list(config.keys())[2]
    auth_header = generate_auth_header(unknown_op_bearer_id)

    response = client.get("/v1/protected-resource", headers=auth_header)
    assert response.status_code == 403


def test_protected_resource_with_http_verb_permission():
    # Get the bearer ID for the fourth user (with HTTP_VERB:GET permission)
    http_verb_bearer_id = list(config.keys())[3]
    auth_header = generate_auth_header(http_verb_bearer_id)

    response = client.get("/v1/protected-resource", headers=auth_header)
    assert response.status_code == 200
    assert response.json() == {"success": True}

    # Test that other HTTP methods are not allowed
    response = client.post("/v1/protected-resource", headers=auth_header)
    assert response.status_code == 403
