from pydantic import BaseModel
from typing_extensions import Literal, Optional

from Schemas_ses.enumeration.enums import StudiesLevel, LocalType
from Schemas_ses.models.model import AnnexeModel
from Schemas_ses.type.types import Year


class TeacherFurniture(BaseModel):
    teacher_desk_with_chair: Optional[int]
    cupboard_or_closet: Optional[int]


Good_or_bad = Literal['Bon / Acceptable', 'Mauvais']


class Office(AnnexeModel):
    name: str
    study_years: Optional[StudiesLevel]
    local_type: Optional[LocalType]
    year_of_commissioning: Optional[Year]
    is_unused: Optional[bool]
    wall_material: Optional[Literal["En dur", "Semi-dur / banco", "Autre: Planche / bambou", "Sans mur"]]
    wall_condition: Optional[Good_or_bad]
    roof_material: Optional[Literal["Tôles", "Tuiles / Fibro ciment / Dalles", "Banco", "Paille", "Sans toit"]]
    roof_condition: Optional[Good_or_bad]
    door_material: Optional[Literal["Métallique", "Tôle / Bois", "Non installées"]]
    window_nature: Optional[Literal["Persiennes", "Volets", "Claustras", "Non installées"]]
    funding: Optional[Literal["Collectivités locales", "APE", "Aide extérieure", "Autres / Non déterminé"]]
    teacher_furniture: TeacherFurniture
    # add student_furniture
    surface_area: Optional[float]
    blackboard: Optional[int]


class OfficeAndFurniture(AnnexeModel):
    """Se réfère à la section Locaux Et Mobiliers"""
    offices: Optional[list[Office]]
