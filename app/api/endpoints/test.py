# TODO: Remove this file, use it as a reference when adding other endpoints for API

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from app.api import deps
from app.models import Test
from app.api.deps import get_current_user

router = APIRouter()


class TestInput(BaseModel):
    test_name: str


@router.get("/")  # this endpoint has prefix /test, so this endpoint is just .../test
async def test_endpoint():
    return {"1": "hello", "2": "byebye"}


@router.post("/add")
async def add_test_endpoint(
    payload: TestInput, session: AsyncSession = Depends(deps.get_session)
):
    new_test = Test(test_name=payload.test_name)
    session.add(new_test)
    await session.commit()

    return f"ADDED NEW USER {payload.test_name}"


@router.get("/specific_test")
async def get_test_endpoint_by_name(
    test_name,
    session: AsyncSession = Depends(deps.get_session),
    _=Depends(get_current_user),
):
    wanted_test = select(Test).where(Test.test_name == test_name)
    result = await session.execute(wanted_test)
    test = result.scalar_one_or_none()

    return test
