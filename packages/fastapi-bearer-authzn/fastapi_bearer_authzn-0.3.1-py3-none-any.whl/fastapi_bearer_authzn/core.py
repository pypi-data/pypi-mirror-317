import hashlib
import hmac
import json
import logging
import os
import re
from secrets import token_urlsafe
from uuid import uuid4

from fastapi import HTTPException, Request, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import (
    BaseModel,
    Field,
    RootModel,
    field_validator,
    model_validator,
)
from typing_extensions import Dict, List, Self, Tuple, Union

# Constants
UUID4_REGEX = r"(?P<api_key_identifier>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})"
SECRET_REGEX = r"(?P<api_key_secret>[A-Za-z0-9_-]{43})"
API_KEY_REGEX = f"^fastapi_bearer_authzn_{UUID4_REGEX}_{SECRET_REGEX}$"
HTTP_VERB_PREFIX = "HTTP_VERB:"


class PermissionConfig(BaseModel):
    hashed_token: str = Field(
        default=..., description="The SHA-3-512 hash of the secret."
    )
    user_identifier: str = Field(
        default=None, description="An optional unique identifier."
    )
    permissions: List[str] = Field(
        default=[], description="The permissions granted to this API Key"
    )


class ConfigModel(RootModel):
    root: Dict[str, PermissionConfig]

    @model_validator(mode="after")
    def validate_keys(self: Self) -> Self:
        for key in self.root.keys():
            if not re.match(pattern=UUID4_REGEX, string=key):
                raise ValueError(f"Key '{key}' is not a valid UUID4.")
        return self


class BearerToken(BaseModel):
    identifier: str = Field(
        default=...,
        pattern=UUID4_REGEX,
    )
    secret: str = Field(default=..., min_length=43, max_length=43)

    @field_validator("secret")
    @classmethod
    def validate_secret(cls, v) -> str:
        if not re.match(pattern=SECRET_REGEX, string=v):
            raise ValueError("Invalid secret format.")
        return v


# FastAPI Dependency
class BearerAuthDependency:
    config: ConfigModel

    def __init__(
        self, config: Union[ConfigModel, None] = None, from_env: bool = False
    ) -> None:
        # Load and parse the configuration from the environment variable
        if config is None and from_env:
            config_str: Union[str, None] = os.getenv(key="FASTAPI_BEARER_AUTHZN_CONFIG")
            if not config_str:
                raise RuntimeError(
                    "FASTAPI_BEARER_AUTHZN_CONFIG environment variable is not set."
                )
            self.config: ConfigModel = ConfigModel.model_validate(
                obj=json.loads(s=config_str)
            )
        elif config is not None and not from_env:
            self.config = ConfigModel.model_validate(obj=config)
        else:
            raise RuntimeError(
                "Invalid configuration. Must use either `config` or `from_env` keyword."
            )

    def __call__(
        self,
        request: Request,
        credentials: HTTPAuthorizationCredentials = Security(dependency=HTTPBearer()),
    ) -> str:
        user_identifier: str = self.authenticate(credentials=credentials)
        logging.debug(f"Authentication successful. Authed ID: {user_identifier}")
        operation_id: Union[str, None] = self.get_operation_id(request)
        if operation_id is None:
            raise HTTPException(status_code=500, detail="Operation ID not found")
        self.authorize(user_identifier=user_identifier, operation_id=operation_id, http_method=request.method)
        logging.debug("Authorization successful")
        return user_identifier

    def get_operation_id(self, request: Request) -> Union[str, None]:
        route = request.scope.get("route")
        if route is None or not hasattr(route, "unique_id"):
            return None
        return route.unique_id

    def parse_bearer_token(self, token: str) -> BearerToken:
        match: Union[re.Match[str], None] = re.match(
            pattern=API_KEY_REGEX, string=token
        )
        if not match:
            raise HTTPException(status_code=403, detail="Invalid bearer token format.")

        return BearerToken(
            identifier=match.group("api_key_identifier"),
            secret=match.group("api_key_secret"),
        )

    def authenticate(self, credentials: HTTPAuthorizationCredentials) -> str:
        token: BearerToken = self.parse_bearer_token(token=credentials.credentials)

        if token.identifier not in self.config.root:
            raise HTTPException(
                status_code=403,
                detail="Authentication failed. Token not found in config.",
            )

        stored_hash: str = self.config.root[token.identifier].hashed_token
        provided_hash: str = hashlib.sha3_512(token.secret.encode()).hexdigest()

        if not hmac.compare_digest(stored_hash, provided_hash):
            raise HTTPException(
                status_code=403,
                detail="Authentication failed. Token verification failed.",
            )

        return token.identifier

    def authorize(self, user_identifier: str, operation_id: str, http_method: str) -> None:
        permissions: List[str] = self.config.root[user_identifier].permissions
        if "*" in permissions:
            logging.debug("Authorization succeeded because of '*'-authorization.")
            return
        
        http_verb_permission = f"{HTTP_VERB_PREFIX}{http_method}"
        if http_verb_permission not in permissions and operation_id not in permissions:
            raise HTTPException(status_code=403, detail="Authorization failed.")


def bootstrap_config(no_identities: int = 3) -> Tuple[Dict[str, dict], Dict[str, dict]]:
    tokens = {}
    for _ in range(no_identities):
        bearer_id = str(uuid4())
        secret = token_urlsafe(32)
        token = f"fastapi_bearer_authzn_{bearer_id}_{secret}"
        tokens[bearer_id] = {"secret": secret, "token": token}
    config = {}
    for bearer_id, token in tokens.items():
        config[bearer_id] = {
            "hashed_token": hashlib.sha3_512((token["secret"]).encode()).hexdigest(),
            "user_identifier": f"user_{uuid4()}@example.com",
            "permissions": ["*"],
        }
    return config, tokens
