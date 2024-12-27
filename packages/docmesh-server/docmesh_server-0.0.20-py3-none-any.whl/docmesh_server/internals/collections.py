from typing import Any
from pydantic import BaseModel

from fastapi import status, APIRouter, Response, Depends

from docmesh_core.db.neo.paper import add_paper
from docmesh_core.db.neo.collection import add_collection, add_paper_to_collection
from docmesh_core.utils.semantic_scholar import get_paper_id
from docmesh_server.dependencies import check_admin_access_token

router = APIRouter(prefix="/collections", dependencies=[Depends(check_admin_access_token)])


class CollectionBody(BaseModel):
    collection_name: str


class CollectionPaperBody(BaseModel):
    collection_name: str
    paper: str


@router.post("/add")
def add_collection_api(
    body: CollectionBody,
    response: Response,
) -> dict[str, Any]:
    try:
        add_collection(collection_name=body.collection_name)
        data = {
            "msg": f"Successfully add a new collection {body.collection_name}.",
        }
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        data = {
            "msg": f"Failed to add a new collection {body.collection_name}, with error: {e}.",
        }

    return {"data": data}


@router.post("/add_paper")
def add_collection_paper_api(
    body: CollectionPaperBody,
    response: Response,
) -> dict[str, Any]:
    semantic_scholar_paper_id = get_paper_id(body.paper)

    if semantic_scholar_paper_id is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        data = {
            "msg": f"Failed to add {body.paper} to collection, cannot find semantic scholar paper id.",
        }
    else:
        try:
            paper_id = add_paper(paper_id=semantic_scholar_paper_id).paper_id
            add_paper_to_collection(paper_id=paper_id, collection_name=body.collection_name)
            data = {
                "msg": f"Successfully add paper {body.paper} to collection {body.collection_name}.",
            }
        except Exception as e:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            data = {
                "msg": f"Failed to add paper {body.paper} to collection {body.collection_name} with error: {e}.",
            }

    return {"data": data}
