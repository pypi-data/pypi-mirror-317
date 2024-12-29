from typing_extensions import TypedDict, Optional

from Schemas_ses.models.model import AnnexeModel


class SexeCount(TypedDict):
    M: Optional[int]
    F: Optional[int]


class ExamCategoryResults(AnnexeModel):
    inscrits: SexeCount
    ont_compose: SexeCount
    admis: SexeCount


class ExamResult(AnnexeModel):
    """"""
    cep: ExamCategoryResults
    cep_vie_active: ExamCategoryResults
