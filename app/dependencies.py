from typing import Annotated

from fastapi import Header, HTTPException


async def get_query_token():
    print("hello one")


async def get_token_header():
    print("hello two")
