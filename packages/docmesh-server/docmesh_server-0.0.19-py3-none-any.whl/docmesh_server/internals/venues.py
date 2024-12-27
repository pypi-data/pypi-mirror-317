from typing import Any
from pydantic import BaseModel

from fastapi import status, APIRouter, Response, Depends

from docmesh_core.db.neo.venue import add_venue, add_collection_to_venue
from docmesh_server.dependencies import check_admin_access_token

router = APIRouter(prefix="/venues", dependencies=[Depends(check_admin_access_token)])


class VenueBody(BaseModel):
    venue_name: str


class VenueCollectionBody(BaseModel):
    venue_name: str
    collection_name: str


@router.post("/add")
def add_venue_api(
    body: VenueBody,
    response: Response,
) -> dict[str, Any]:
    try:
        add_venue(venue_name=body.venue_name)
        data = {
            "msg": f"Successfully add a new venue {body.venue_name}.",
        }
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        data = {
            "msg": f"Failed to add a new venue {body.venue_name}, with error: {e}.",
        }

    return {"data": data}


@router.post("/add_collection")
def add_venue_collection_api(
    body: VenueCollectionBody,
    response: Response,
) -> dict[str, Any]:
    try:
        add_collection_to_venue(collection_name=body.collection_name, venue_name=body.venue_name)
        data = {
            "msg": f"Successfully add collection {body.collection_name} to venue {body.venue_name}.",
        }
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        data = {
            "msg": f"Failed to add collection {body.collection_name} to venue {body.venue_name} with error {e}.",
        }

    return {"data": data}
