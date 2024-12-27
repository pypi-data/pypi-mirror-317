from typing import Any
from pydantic import BaseModel

from fastapi import status, APIRouter, Response, Depends

from docmesh_core.db.neo.graph import list_cite_graph
from docmesh_server.dependencies import check_access_token, EntityInfo

router = APIRouter(prefix="/graphs")


class CiteBody(BaseModel):
    n: int


@router.post("/cite")
def list_cite_graph_api(
    body: CiteBody,
    response: Response,
    entity_info: EntityInfo = Depends(check_access_token),
) -> dict[str, Any]:
    entity_name = entity_info.entity_name

    try:
        nodes, edges = list_cite_graph(entity_name=entity_name, n=body.n)

        data = {
            "msg": f"Successfully get cite graph of {entity_name}.",
            "nodes": nodes,
            "edges": edges,
        }
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        data = {
            "msg": f"Failed to get cite graph of {entity_name} with error: {e}.",
        }

    return {"data": data}
