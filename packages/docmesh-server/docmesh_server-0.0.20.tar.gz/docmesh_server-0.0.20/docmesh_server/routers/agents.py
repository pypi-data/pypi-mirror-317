import os

from typing import Any
from pydantic import BaseModel

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from docmesh_agent.agent import execute_docmesh_agent, aexecute_docmesh_agnet
from docmesh_server.dependencies import check_access_token, EntityInfo

router = APIRouter(prefix="/agents")


class AgentBody(BaseModel):
    session_id: str
    query: str
    style: bool = True


class PosterBody(BaseModel):
    pdf_link: str
    model: str = "gpt-4o-mini"


@router.post("/execute")
def execute_docmesh_agent_api(
    body: AgentBody,
    entity_info: EntityInfo = Depends(check_access_token),
) -> dict[str, Any]:
    if entity_info.premium:
        model = os.getenv("PREMIUM_MODEL")
    else:
        model = os.getenv("BASIC_MODEL")

    msg = execute_docmesh_agent(
        entity_name=entity_info.entity_name,
        model=model,
        query=body.query,
        session_id=body.session_id,
        style=body.style,
    )
    data = {"query": body.query, "msg": msg}
    return {"data": data}


@router.post("/aexecute")
async def aexecute_docmesh_agnet_api(
    body: AgentBody,
    entity_info: EntityInfo = Depends(check_access_token),
) -> StreamingResponse:
    if entity_info.premium:
        model = os.getenv("PREMIUM_MODEL")
    else:
        model = os.getenv("BASIC_MODEL")

    return StreamingResponse(
        aexecute_docmesh_agnet(
            entity_name=entity_info.entity_name,
            model=model,
            query=body.query,
            session_id=body.session_id,
            style=body.style,
        )
    )
