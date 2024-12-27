from typing import Any
from pydantic import BaseModel

from fastapi import status, APIRouter, Response, Depends

from docmesh_core.db.auth import add_auth_for_entity, refresh_premium
from docmesh_core.db.neo.entity import add_entity, DuplicateEntity
from docmesh_server.database import engine
from docmesh_server.dependencies import check_admin_access_token

router = APIRouter(prefix="/admin", dependencies=[Depends(check_admin_access_token)])


class EntityBody(BaseModel):
    entity_name: str


class RefreshPremiumBody(BaseModel):
    entity_name: str
    days: int


@router.post("/add_entity")
def add_entity_api(
    body: EntityBody,
    response: Response,
) -> dict[str, Any]:
    try:
        add_entity(entity_name=body.entity_name)
        access_token = add_auth_for_entity(engine, entity_name=body.entity_name)

        data = {
            "entity_name": body.entity_name,
            "access_token": access_token,
            "msg": f"Successfully add a new entity {body.entity_name}.",
        }
    except DuplicateEntity:
        response.status_code = status.HTTP_405_METHOD_NOT_ALLOWED
        data = {
            "msg": f"Failed to add a new entity, {body.entity_name} already existed.",
        }
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        data = {
            "msg": f"Failed to add a new entity {body.entity_name}, with error {e}.",
        }

    return {"data": data}


@router.post("/refresh_premium")
def refresh_premium_api(
    body: RefreshPremiumBody,
    response: Response,
) -> dict[str, Any]:
    try:
        expiration_date = refresh_premium(engine, entity_name=body.entity_name, days=body.days)

        data = {
            "expiration_date": expiration_date.strftime("%Y-%m-%d %H:%M:%S"),
            "msg": f"Successfully refresh entity {body.entity_name} premium to {expiration_date}.",
        }
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        data = {
            "msg": f"Failed to refresh entity {body.entity_name} premium expiration date, with error {e}.",
        }

    return {"data": data}
