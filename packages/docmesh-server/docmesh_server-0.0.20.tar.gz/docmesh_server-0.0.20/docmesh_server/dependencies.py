from pydantic import BaseModel

from fastapi import status, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from docmesh_core.db.auth import get_entity_from_auth, log_last_login
from docmesh_server.database import engine

auth_scheme = HTTPBearer()


class EntityInfo(BaseModel):
    entity_name: str
    premium: bool


def check_access_token(
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
) -> EntityInfo:
    access_token = token.credentials
    entity_name, premium = get_entity_from_auth(engine, access_token)

    if entity_name is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect bearer token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        log_last_login(engine, entity_name=entity_name)

    entity_info = EntityInfo(entity_name=entity_name, premium=premium)

    return entity_info


def check_admin_access_token(
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
) -> None:
    access_token = token.credentials
    entity_name, _ = get_entity_from_auth(engine, access_token)

    if entity_name != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect bearer token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        log_last_login(engine, entity_name=entity_name)
