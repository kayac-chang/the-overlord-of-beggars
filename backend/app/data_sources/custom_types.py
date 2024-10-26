import unicodedata
from pydantic import BeforeValidator
from typing_extensions import Annotated


def fWidth2hWidth(source:str):
    return unicodedata.normalize('NFKC', source)

CustomAddress=Annotated[str,BeforeValidator(fWidth2hWidth)]
