from typing import Any
from pydantic import BaseModel

from fastapi import status, APIRouter, Response, Depends

from docmesh_core.db.neo.paper import get_paper
from docmesh_server.dependencies import check_admin_access_token

router = APIRouter(prefix="/pdfs", dependencies=[Depends(check_admin_access_token)])


class PDFBody(BaseModel):
    paper_id: str
    pdf: str


@router.post("/update")
def update_pdf_api(
    body: PDFBody,
    response: Response,
) -> dict[str, Any]:

    try:
        paper = get_paper(paper=body.paper_id)
        paper.pdf = body.pdf
        paper.save()

        data = {
            "msg": f"Successfully update paper {body.paper_id} pdf link as {body.pdf}.",
        }
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        data = {
            "msg": f"Failed to update paper pdf link with error: {e}.",
        }

    return {"data": data}
