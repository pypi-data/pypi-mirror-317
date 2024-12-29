from typing import Optional

from typing_extensions import Literal

from Schemas_ses.models.model import AnnexeModel


class ParticipatorySchoolManagement(AnnexeModel):
    """"""
    is_ape_office_functional: Optional[bool]
    has_all_required_members: Optional[bool]
    num_meetings_previous_year: Optional[int]
    num_general_assemblies_previous_year: Optional[int]
    num_assemblies_budget: Optional[int]
    num_assemblies_academic_results: Optional[int]
    other_assembly_themes: Optional[
        list[Literal["Environnement", "Santé",
        "Kit Scolaire", "Maintien des enfants à l'école"]]]
    result_communication_methods: Optional[
        list[Literal[
            "Carnet de correspondance",
            "Réunion APE",
            "AG",
            "Echange avec les parents concerné"
        ]]]
    has_development_education_projects: Optional[bool]
