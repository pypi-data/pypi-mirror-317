from typing import Any
from pydantic import BaseModel

from fastapi import status, APIRouter, Response, Depends

from docmesh_core.db.message import get_messages
from docmesh_server.database import engine
from docmesh_server.dependencies import check_access_token, EntityInfo

router = APIRouter(prefix="/sessions")


class SessionBody(BaseModel):
    session_id: str


@router.get("/{session_id}")
def get_session_messages(
    session_id: str,
    response: Response,
    entity_info: EntityInfo = Depends(check_access_token),
) -> dict[str, Any]:
    entity_name = entity_info.entity_name

    try:
        messages = get_messages(
            engine,
            entity_name=entity_name,
            session_id=session_id,
        )
        data = {
            "msg": f"Successfully get messages of session {session_id}.",
            "messages": messages,
        }
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        data = {
            "msg": f"Failed to get messages fo session {session_id} with error: {e}.",
        }

    return {"data": data}
