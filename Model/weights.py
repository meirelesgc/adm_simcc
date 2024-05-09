from pydantic import UUID4, BaseModel


class Weights(BaseModel):
    name: str
    institution_id: UUID4
    A1: float
    A2: float
    A3: float
    A4: float
    B1: float
    B2: float
    B3: float
    B4: float
    C: float
    SQ: float
    BOOK: float
    BOOK_CHAPTER: float
    F1: float = 0
    F2: float = 0
    F3: float = 0
    F4: float = 0
    F5: float = 0

    @property
    def SOFTWARE(self) -> float:
        return self.F5

    @property
    def PATENT_GRANTED(self) -> float:
        return self.F3

    @property
    def PATENT_NOT_GRANTED(self) -> float:
        return self.F1

    @property
    def REPORT(self) -> float:
        return self.F4
