from typing import Any
from pydantic import BaseModel

from fastapi import status, APIRouter, Response, Depends

from docmesh_agent.embeddings import update_paper_embeddings
from docmesh_server.dependencies import check_admin_access_token

router = APIRouter(prefix="/embeddings", dependencies=[Depends(check_admin_access_token)])


class EmbeddingsBody(BaseModel):
    n: int


@router.post("/update")
def update_embeddings_api(
    body: EmbeddingsBody,
    response: Response,
) -> dict[str, Any]:

    try:
        update_cnt = update_paper_embeddings(n=body.n)
        data = {
            "update_cnt": update_cnt,
            "msg": f"Successfully update {update_cnt} papers embeddings.",
        }
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        data = {
            "update_cnt": 0,
            "msg": f"Failed to update papers embeddings with error: {e}.",
        }

    return {"data": data}
