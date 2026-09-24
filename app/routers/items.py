from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from ..database import get_session
from ..models import Item, ItemStatus
from ..schemas import ItemCreate, ItemUpdate

router = APIRouter(prefix="/items", tags=["Task 1 - Lost & Found"])


@router.post("", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item_data: ItemCreate, session: Session = Depends(get_session)):
    item = Item(**item_data.model_dump())
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


# These routes are declared before /items/{item_id} so "status" and "category"
# are interpreted as route words rather than integer IDs.
@router.get("/status/{item_status}", response_model=list[Item])
def get_items_by_status(
    item_status: ItemStatus,
    session: Session = Depends(get_session),
):
    statement = select(Item).where(Item.status == item_status)
    return session.exec(statement).all()


@router.get("/category/{category}", response_model=list[Item])
def get_items_by_category(
    category: str,
    session: Session = Depends(get_session),
):
    statement = select(Item).where(Item.category == category)
    return session.exec(statement).all()


@router.get("", response_model=list[Item])
def get_items(session: Session = Depends(get_session)):
    return session.exec(select(Item)).all()


@router.get("/{item_id}", response_model=Item)
def get_item(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    return item


@router.put("/{item_id}", response_model=Item)
def update_item(
    item_id: int,
    item_data: ItemUpdate,
    session: Session = Depends(get_session),
):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )

    update_data = item_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)

    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )

    session.delete(item)
    session.commit()
    return None
