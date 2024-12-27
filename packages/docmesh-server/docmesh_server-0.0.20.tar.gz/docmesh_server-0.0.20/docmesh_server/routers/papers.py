from typing import Any
from pydantic import BaseModel

from fastapi import status, APIRouter, Response, Depends

from docmesh_core.db.neo.paper import add_paper, get_paper, get_papers, PaperNotFound, PDFNotFound
from docmesh_core.db.neo.entity import mark_paper_read, save_paper_list, is_paper_read, is_paper_in_list
from docmesh_core.utils.semantic_scholar import get_paper_id
from docmesh_agent.utils import extract_figures_from_paper
from docmesh_server.dependencies import check_access_token, EntityInfo

router = APIRouter(prefix="/papers")


class PaperBody(BaseModel):
    paper: str


class PaperIdBody(BaseModel):
    paper_id: str


class PapersBody(BaseModel):
    papers: list[str]


@router.get("/{paper}", dependencies=[Depends(check_access_token)])
def get_paper_api(
    paper: str,
    response: Response,
) -> dict[str, Any]:

    try:
        paper_details = get_paper(paper=paper).serialize
        data = {
            "msg": f"Successfully get paper details of {paper}.",
            "details": paper_details,
        }
    except PaperNotFound:
        response.status_code = status.HTTP_404_NOT_FOUND
        data = {
            "msg": f"{paper} not found in database.",
        }
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        data = {
            "msg": f"Failed to get paper details of {paper} with error: {e}.",
        }

    return {"data": data}


@router.post("/batch", dependencies=[Depends(check_access_token)])
def get_papers_api(
    body: PapersBody,
    response: Response,
) -> dict[str, Any]:

    try:
        papers = get_papers(body.papers)
        papers_details = [paper.serialize if paper is not None else None for paper in papers]
        data = {
            "msg": "Successfully get papers details.",
            "details": papers_details,
        }
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        data = {
            "msg": f"Failed to get papers details with error: {e}.",
        }

    return {"data": data}


@router.post("/add")
def add_paper_api(
    body: PaperBody,
    response: Response,
    entity_info: EntityInfo = Depends(check_access_token),
) -> dict[str, Any]:
    semantic_scholar_paper_id = get_paper_id(body.paper)

    if semantic_scholar_paper_id is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        data = {
            "msg": f"Failed to add a new paper {body.paper}, cannot find semantic scholar paper id.",
        }
    else:
        try:
            paper_id = add_paper(paper_id=semantic_scholar_paper_id).paper_id
            data = {
                "msg": f"Successfully add a new paper {body.paper} with paper id {paper_id}.",
            }
        except Exception as e:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            data = {
                "msg": f"Failed to add a new paper {body.paper}, with error: {e}.",
            }

    return {"data": data}


@router.post("/is_read")
def is_paper_read_api(
    body: PaperBody,
    response: Response,
    entity_info: EntityInfo = Depends(check_access_token),
) -> dict[str, Any]:
    entity_name = entity_info.entity_name
    semantic_scholar_paper_id = get_paper_id(body.paper)

    if semantic_scholar_paper_id is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        data = {
            "msg": f"Failed to check if paper {body.paper} is read, cannot find semantic scholar paper id.",
        }
    else:
        result = is_paper_read(entity_name=entity_name, paper_id=semantic_scholar_paper_id)
        data = {
            "msg": f"Successfully check if paper {body.paper} is read.",
            "result": result,
        }

    return {"data": data}


@router.post("/is_in_list")
def is_paper_in_list_api(
    body: PaperBody,
    response: Response,
    entity_info: EntityInfo = Depends(check_access_token),
) -> dict[str, Any]:
    entity_name = entity_info.entity_name
    semantic_scholar_paper_id = get_paper_id(body.paper)

    if semantic_scholar_paper_id is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        data = {
            "msg": f"Failed to check if paper {body.paper} is in reading list, cannot find semantic scholar paper id.",
        }
    else:
        result = is_paper_in_list(entity_name=entity_name, paper_id=semantic_scholar_paper_id)
        data = {
            "msg": f"Successfully check if paper {body.paper} is in reading list.",
            "result": result,
        }

    return {"data": data}


@router.post("/add_and_mark")
def add_and_mark_paper_api(
    body: PaperBody,
    response: Response,
    entity_info: EntityInfo = Depends(check_access_token),
) -> dict[str, Any]:
    entity_name = entity_info.entity_name
    semantic_scholar_paper_id = get_paper_id(body.paper)

    if semantic_scholar_paper_id is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        data = {
            "msg": f"Failed to add and mark paper {body.paper}, cannot find semantic scholar paper id.",
        }
    else:
        try:
            paper_id = add_paper(paper_id=semantic_scholar_paper_id).paper_id
            mark_paper_read(entity_name=entity_name, paper_id=paper_id)
            data = {
                "msg": (
                    f"Successfully add and mark paper {body.paper} read with paper id {paper_id} for {entity_name}."
                ),
            }
        except Exception as e:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            data = {
                "msg": f"Failed to add and mark paper {body.paper} read with error: {e}.",
            }

    return {"data": data}


@router.post("/mark_paper_id")
def mark_paper_id_api(
    body: PaperIdBody,
    response: Response,
    entity_info: EntityInfo = Depends(check_access_token),
) -> dict[str, Any]:
    entity_name = entity_info.entity_name

    try:
        paper_id = add_paper(paper_id=body.paper_id).paper_id
        mark_paper_read(entity_name=entity_name, paper_id=paper_id)
        data = {
            "msg": f"Successfully add and mark paper id {paper_id} read for {entity_name}.",
        }
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        data = {
            "msg": f"Failed to add and mark paper id {paper_id} read with error: {e}.",
        }

    return {"data": data}


@router.post("/add_and_save")
def add_and_save_paper_api(
    body: PaperBody,
    response: Response,
    entity_info: EntityInfo = Depends(check_access_token),
) -> dict[str, Any]:
    entity_name = entity_info.entity_name
    semantic_scholar_paper_id = get_paper_id(body.paper)

    if semantic_scholar_paper_id is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        data = {
            "msg": f"Failed to add and save paper {body.paper}, cannot find semantic scholar paper id.",
        }
    else:
        try:
            paper_id = add_paper(paper_id=semantic_scholar_paper_id).paper_id
            save_paper_list(entity_name=entity_name, paper_id=paper_id)
            data = {
                "msg": (
                    f"Successfully add and save paper {body.paper} to list with paper id {paper_id} for {entity_name}."
                ),
            }
        except Exception as e:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            data = {
                "msg": f"Failed to add and save paper {body.paper} to list with error: {e}.",
            }

    return {"data": data}


@router.post("/extract_figures")
def extract_figures_api(
    body: PaperBody,
    response: Response,
    entity_info: EntityInfo = Depends(check_access_token),
) -> dict[str, Any]:
    semantic_scholar_paper_id = get_paper_id(body.paper)

    if semantic_scholar_paper_id is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        data = {
            "msg": f"Failed to extract figures of paper {body.paper}, cannot find semantic scholar paper id.",
        }
    else:
        try:
            paper_id = add_paper(paper_id=semantic_scholar_paper_id).paper_id
            figures = extract_figures_from_paper(paper_id=paper_id)

            data = {
                "msg": f"Successfully extract figures of paper {body.paper}.",
                "figures": figures,
            }
        except PDFNotFound:
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
            data = {
                "msg": f"Failed to extract figures of paper {body.paper}, cannot find pdf.",
            }
        except Exception as e:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            data = {
                "msg": f"Failed to extract figures of paper {body.paper} with error: {e}.",
            }

    return {"data": data}
