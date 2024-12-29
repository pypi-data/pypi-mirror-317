from typing import List, Dict

from typing_extensions import Optional

from Schemas_ses.models.model import AnnexeModel


class PedagogicalMaterial(AnnexeModel):
    name: str
    quantities_by_grade: Dict[str, Optional[int]]


class ListPedagogicalMaterials(AnnexeModel):
    materials: List[PedagogicalMaterial]


class CollectiveEquipment(AnnexeModel):
    pedagogical_kits: Optional[int]
    geographic_wall_maps: Optional[int]
    metric_compendiums: Optional[int]
    geometric_compendiums: Optional[int]
    scientific_compendiums: Optional[int]
    scientific_boards: Optional[int]
    desktop_computers: Optional[int]
    image_boxes: Optional[int]
    printers: Optional[int]
    dictionaries: Optional[int]
    polyhedron_boxes: Optional[int]
    photocopiers: Optional[int]
    terrestrial_globes: Optional[int]


class TeachingAndLearningEquipment(AnnexeModel):
    """"""
    collective_equipment: CollectiveEquipment
    teacher_pedagogical_materials: ListPedagogicalMaterials
    student_pedagogical_materials: ListPedagogicalMaterials
