from sqlmodel import SQLModel


class Paging(SQLModel):
    offset: int
    limit: int


class QueryParams(SQLModel):
    paging: Paging
