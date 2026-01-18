# TODO: Remove this file, use it as a reference when adding other endpoints for API

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api import deps
from app.models import Test

router = APIRouter()

@router.get("/") # this endpoint has prefix /test, so this endpoint is just .../test
async def test_endpoint():
    return { "1": "hello", "2": "byebye" }

@router.post("/add")
async def add_test_endpoint(test_name, session: AsyncSession = Depends(deps.get_session)):
    new_test = Test(
        test_name=test_name
    )
    session.add(new_test)
    await session.commit()
    
    return "ADDED NEW USER"

@router.get("/specific_test")
async def get_test_endpoint_by_name(test_name, session: AsyncSession = Depends(deps.get_session)):
    wanted_test = select(Test).where(Test.test_name == test_name)
    result = await session.execute(wanted_test)
    test = result.scalar_one_or_none()

    return test