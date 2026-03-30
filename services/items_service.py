from app.errors import ResourceNotFoundError
from app.state import DemoState
from models.common import Priority, WorkItemStatus
from models.item import WorkItem


class ItemService:
    def __init__(self, state: DemoState) -> None:
        self._state = state

    def list_items(
        self,
        *,
        status: WorkItemStatus | None = None,
        priority: Priority | None = None,
        label: str | None = None,
    ) -> list[WorkItem]:
        items = list(self._state.items.values())
        if status is not None:
            items = [item for item in items if item.status is status]
        if priority is not None:
            items = [item for item in items if item.priority is priority]
        if label:
            normalized = label.strip().lower()
            items = [item for item in items if normalized in (value.lower() for value in item.labels)]
        return sorted(items, key=lambda item: (item.priority.sort_rank, item.title))

    def get_item(self, item_id: str) -> WorkItem:
        item = self._state.items.get(item_id)
        if item is None:
            raise ResourceNotFoundError("item", item_id)
        return item
