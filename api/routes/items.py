from fastapi import APIRouter, Depends, Query

from app.dependencies import get_item_service
from contracts.item import ItemDetailContract, ItemListContract, ItemSummaryContract
from models.common import Priority, WorkItemStatus
from services.items_service import ItemService


router = APIRouter(tags=["items"])


def _to_summary(item) -> ItemSummaryContract:
    return ItemSummaryContract(
        id=item.id,
        title=item.title,
        summary=item.summary,
        priority=item.priority,
        status=item.status,
        labels=list(item.labels),
        active_session_ids=list(item.active_session_ids),
    )


def _to_detail(item) -> ItemDetailContract:
    return ItemDetailContract(
        **_to_summary(item).model_dump(),
        target_outcome=item.target_outcome,
        open_questions=list(item.open_questions),
        active_agent_ids=list(item.active_agent_ids),
        updated_at=item.updated_at.isoformat(),
    )


@router.get("/items", response_model=ItemListContract)
async def list_items(
    status: WorkItemStatus | None = Query(default=None, description="Optional work item status filter."),
    priority: Priority | None = Query(default=None, description="Optional work item priority filter."),
    label: str | None = Query(default=None, description="Optional label filter."),
    service: ItemService = Depends(get_item_service),
) -> ItemListContract:
    items = service.list_items(status=status, priority=priority, label=label)
    return ItemListContract(items=[_to_summary(item) for item in items])


@router.get("/items/{item_id}", response_model=ItemDetailContract)
async def get_item(item_id: str, service: ItemService = Depends(get_item_service)) -> ItemDetailContract:
    return _to_detail(service.get_item(item_id))
