from pydantic import BaseModel
from typing_extensions import Optional

from Schemas_ses.enumeration.enums import SchoolPropertyTitle
from Schemas_ses.models.model import AnnexeModel


class PropertyAndBoundaries(BaseModel):
    """Se réfère à la sous section Propriété et délimitations de l'école"""
    school_property_title: Optional[list[SchoolPropertyTitle]]
    is_school_area_demarcated: Optional[bool]
    is_school_area_fenced: Optional[bool]


class OutdoorFacilities(BaseModel):
    """Se réfère à la sous section Aménagements extérieurs"""
    is_playground_shaded: Optional[bool]
    has_garden_or_school_field: Optional[bool]
    has_adaptations_for_special_needs_children: Optional[bool]


class WaterAndHygieneAccess(BaseModel):
    has_drinking_water_on_site: Optional[bool]
    has_handwashing_facility: Optional[bool]
    has_functional_latrines: Optional[bool]
    has_adapted_latrines_for_special_needs: Optional[bool]
    has_equipped_urinal: Optional[bool]


class SchoolServicesAndEquipment(BaseModel):
    is_electrified: Optional[bool]
    has_functional_canteen: Optional[bool]
    has_kitchen_equipment: Optional[bool]
    has_food_store_in_good_condition: Optional[bool]

    has_functional_library: Optional[bool]
    has_first_aid_kit: Optional[bool]


class ManagementBodies(AnnexeModel):
    has_parents_association: Optional[bool]
    has_mothers_association: Optional[bool]
    has_management_committee: Optional[bool]
    has_teachers_council: Optional[bool]
    has_other_management_committees: Optional[bool]


class SportsFacilities(AnnexeModel):
    has_marked_sports_field: Optional[bool]
    has_equipped_sports_field: Optional[bool]


class GeneralInfo(AnnexeModel):
    """Se réfère à la section Information générale sur l'école"""
    property_and_boundaries: PropertyAndBoundaries
    outdoor_facilities: OutdoorFacilities
    water_and_hygiene_access: WaterAndHygieneAccess
    school_services_and_equipment: SchoolServicesAndEquipment
    management_bodies: ManagementBodies
    sports_facilities: SportsFacilities
