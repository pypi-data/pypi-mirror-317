from pydantic import Field
from typing_extensions import Annotated, Literal

Year = Annotated[int, Field(strict=True, ge=1000, le=9999)]
Length = Annotated[int, Field(strict=True, ge=0)]
Sexe = Literal["M", "F"]