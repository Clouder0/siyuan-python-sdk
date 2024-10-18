"""Raw API wrapper for siyuan"""

from pydantic import BaseModel
from contextlib import contextmanager
from typing import Any, Generic, Literal, Type, TypeVar
import aiohttp

_T = TypeVar("_T")


class APIResponse(Generic[_T], BaseModel):
    code: int
    msg: str
    data: _T

    def get(self) -> _T:
        """
        If success, return data. Otherwise, raise Exception.

        Raises:
            Exception: if API return code is not 0.
        Returns:
            Any: the data field of the API response.
        """
        if self.code != 0:
            raise Exception(self.msg)
        return self.data


class DoOperationResult(BaseModel):
    action: Literal["insert", "update", "delete", "move"]
    data: str
    id: str
    parentID: str
    previousID: str
    nextID: str
    retData: None


class OperationResults(BaseModel):
    doOperations: list[DoOperationResult]
    undoOperations: None


class SiyuanAPI:
    session: aiohttp.ClientSession

    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def post(
        self, url: str, data: dict[str, Any], _: Type[_T] = _T
    ) -> APIResponse[_T]:
        async with self.session.post(url, json=data) as resp:
            res = APIResponse.model_validate_json(await resp.json())
            return res

    async def sql(self, query: str):
        res = await self.post[Any]("/api/sql", {"query": query}, Any)
        return res

    async def insert_block(
        self,
        dataType: Literal["markdown"] | Literal["dom"],
        data: str,
        nextID: str = "",
        previousID: str = "",
        parentID: str = "",
    ):
        if nextID == "" and previousID == "" and parentID == "":
            raise RuntimeError("nextID, previousID and parentID cannot be all empty")
        res = await self.post(
            "/api/block/insertBlock",
            {
                "dataType": dataType,
                "data": data,
                "nextID": nextID,
                "previousID": previousID,
                "parentID": parentID,
            },
            list[OperationResults],
        )
        return res

    async def update_block(
        self, id: str, dataType: Literal["markdown"] | Literal["dom"], data: str
    ):
        res = await self.post(
            "/api/block/updateBlock",
            {
                "id": id,
                "dataType": dataType,
                "data": data,
            },
            list[OperationResults],
        )
        return res

    async def delete_block(self, id: str):
        res = await self.post(
            "/api/block/deleteBlock",
            {
                "id": id,
            },
            list[OperationResults],
        )
        return res

    async def move_block(
        self, id: str, nextID: str = "", previousID: str = "", parentID: str = ""
    ):
        if nextID == "" and previousID == "" and parentID == "":
            raise RuntimeError("nextID, previousID and parentID cannot be all empty")
        res = await self.post(
            "/api/block/moveBlock",
            {
                "id": id,
                "nextID": nextID,
                "previousID": previousID,
                "parentID": parentID,
            },
            list[OperationResults],
        )
        return res

    async def fold_block(self, id: str):
        res = await self.post(
            "/api/block/foldBlock",
            {
                "id": id,
            },
            None,
        )
        return res

    async def unfold_block(self, id: str):
        res = await self.post(
            "/api/block/unfoldBlock",
            {
                "id": id,
            },
            None,
        )
        return res


@contextmanager
def api_session(url: str = "http://127.0.0.1:6806", token: str = ""):
    session = aiohttp.ClientSession(
        base_url=url,
        headers={"Content-Type": "application/json", "Authorization": f"Token {token}"},
    )
    try:
        yield SiyuanAPI(session)
    finally:
        session.close()
