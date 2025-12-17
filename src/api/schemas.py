from pydantic import BaseModel, Field
# from pydantic.generics import GenericModel
from typing import Optional, Generic, TypeVar, List, Literal


class GenericResponse(BaseModel):
    message: str = Field(description="Сообщение, поясняющее суть ответа")
    record_id: Optional[str] = Field(default=None, description='id обработанной записи')


class GenericListResponse(BaseModel):
    message: str = Field(description="Сообщение, поясняющее суть ответа")
    record_ids: Optional[list] = Field(default=None, description='id обработанной записи')


class GenericErrorResponse(BaseModel):
    message: str = Field(description="Сообщение, поясняющее суть ошибки")
    error: str | None = Field(description='Ошибка')


T = TypeVar("T")
S = TypeVar("S", bound=str)


class ServerResponse(BaseModel, Generic[T]):
    data: T = Field(description="Данные ответа")
    success: bool = Field(description="Успешность обработки данных при формировании ответа")
    message: str = Field(description="Сообщение, поясняющее суть ответа")
    status: int = Field(default=200, description="Код ответа")


class ServerErrorResponse(BaseModel):
    data: None = Field(default=None, description="Данные ответа")
    success: bool = Field(default=False, description="Успешность обработки данных при формировании ответа")
    message: str = Field(description="Сообщение, поясняющее суть ответа")
    status: int = Field(description="Код ответа")


class ServerErrorResponse400(ServerErrorResponse):
    status: int = Field(default=400, description="Код ответа")


class ServerErrorResponse404(ServerErrorResponse):
    status: int = Field(default=404, description="Код ответа")


class ServerErrorResponse500(ServerErrorResponse):
    status: int = Field(default=500, description="Код ответа")


class PaginatedData(BaseModel, Generic[T, S]):
    items: List[T] = Field(description="Данные ответа (список)")
    page: int = Field(description="Страница")
    itemsPerPage: int = Field(description="Количество элементов на странице")
    pageCount: int = Field(description="Номер страницы")
    total: int = Field(description="Всего страниц")
    sortField: S = Field(description="Сортировка по полю")
    sortDirection: Literal["asc", "desc"] = Field(description="Направление сортировки")

