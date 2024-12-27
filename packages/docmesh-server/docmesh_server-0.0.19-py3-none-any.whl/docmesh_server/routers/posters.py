import os

from typing import Any
from pydantic import BaseModel

from fastapi import status, APIRouter, Response, Depends

from docmesh_core.db.neo.paper import add_paper, PDFNotFound
from docmesh_core.utils.semantic_scholar import get_paper_id
from docmesh_agent.utils import get_poster_from_db
from docmesh_agent.utils import generate_poster_from_paper
from docmesh_server.dependencies import check_access_token, EntityInfo

router = APIRouter(prefix="/posters")


class PaperBody(BaseModel):
    paper: str


@router.post("/generate")
def generate_poster_api(
    body: PaperBody,
    response: Response,
    entity_info: EntityInfo = Depends(check_access_token),
) -> dict[str, Any]:
    model = os.getenv("BASIC_MODEL")
    semantic_scholar_paper_id = get_paper_id(body.paper)

    if semantic_scholar_paper_id is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        data = {
            "msg": f"Failed to extract figures of paper {body.paper}, cannot find semantic scholar paper id.",
        }
    else:
        try:
            paper = add_paper(paper_id=semantic_scholar_paper_id)
            poster = generate_poster_from_paper(
                paper_id=paper.paper_id,
                entity_name=entity_info.entity_name,
                model=model,
            )

            data = {
                "msg": f"Successfully generate poster of paper {body.paper}.",
                "poster": poster,
            }
        except PDFNotFound:
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
            data = {
                "msg": f"Failed to generate poster of paper {body.paper}, cannot find pdf.",
            }
        except Exception as e:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            data = {
                "msg": f"Failed to generate poster of paper {body.paper} with error: {e}.",
            }

    return {"data": data}


@router.get("/{poster_id}", dependencies=[Depends(check_access_token)])
def get_poster_api(
    poster_id: str,
    response: Response,
) -> dict[str, Any]:

    try:
        poster = get_poster_from_db(poster_id=poster_id)
        data = {
            "msg": f"Successfully get poster details of {poster_id}.",
            "poster": poster,
        }
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        data = {
            "msg": f"Failed to get poster details of {poster_id} with error: {e}.",
        }

    return {"data": data}
