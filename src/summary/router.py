from fastapi import APIRouter, Depends, HTTPException

from src.summary import service
from src.summary.dependencies import verify_api_key
from src.summary.exceptions import (
    InvalidSummaryInputError,
    LLMProviderError,
)
from src.summary.schemas import (
    SummaryRequest,
    SummaryResponse,
)

router = APIRouter(
    prefix="/summary",
    tags=["Summary"],
)


@router.post(
    "",
    response_model=SummaryResponse,
    summary="Generate a text summary",
    dependencies=[Depends(verify_api_key)],
    responses={
        400: {"description": "Empty or oversized input"},
        401: {"description": "Missing or invalid API key"},
        502: {"description": "LLM provider unavailable"},
    },
)
async def create_summary(request: SummaryRequest):

    try:
        return await service.create_summary(request.text)

    except InvalidSummaryInputError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except LLMProviderError as exc:
        raise HTTPException(
            status_code=502,
            detail="Summary generation service unavailable",
        ) from exc
