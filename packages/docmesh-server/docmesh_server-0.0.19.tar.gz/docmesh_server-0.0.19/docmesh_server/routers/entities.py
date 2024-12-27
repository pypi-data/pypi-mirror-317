from typing import Any

from fastapi import status, APIRouter, Response, Depends

from docmesh_core.db.neo.entity import list_reading_list
from docmesh_server.dependencies import check_access_token, EntityInfo

router = APIRouter(prefix="/entities")


@router.get("/name")
def get_entity_name(
    entity_info: EntityInfo = Depends(check_access_token),
) -> dict[str, Any]:
    entity_name = entity_info.entity_name
    data = {"entity_name": entity_name}

    return {"data": data}


@router.get("/reading_list")
def list_reading_list_api(
    response: Response,
    entity_info: EntityInfo = Depends(check_access_token),
) -> dict[str, Any]:
    entity_name = entity_info.entity_name

    try:
        reading_list = list_reading_list(entity_name=entity_name)

        if reading_list.shape[0] == 0:
            reading_list = []
        else:
            reading_list = reading_list.drop(columns=["summary"])
            reading_list = reading_list.to_dict(orient="records")

        data = {
            "msg": f"Successfully get reading list of {entity_name}.",
            "reading_list": reading_list,
        }
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        data = {
            "msg": f"Failed to get reading list of {entity_name} with error: {e}.",
        }

    return {"data": data}
