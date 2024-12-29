from typing_extensions import Optional

from Schemas_ses.enumeration.enums import Distance, SourceEau, TypePollution, SourceElectricity
from Schemas_ses.models.model import AnnexeModel
from Schemas_ses.type.types import Length


class SchoolDistance(AnnexeModel):
    """Se réfère à la section Distance de l'école"""
    distance_to_department_capital: Optional[Distance]
    distance_to_commune_capital: Optional[Distance]
    distance_to_arrondissement_capital: Optional[Distance]
    distance_to_school_district_office: Optional[Distance]
    distance_to_nearest_health_center: Optional[Distance]
    distance_to_nearest_market: Optional[Distance]
    distance_to_farthest_served_village: Optional[Distance]


class SchoolAccessibility(AnnexeModel):
    permanent_access: Optional[bool]
    favorable_season_access: Optional[str]
    paved_road_distance: Optional[Length]
    all_vehicle_track_distance: Optional[Length]
    offroad_vehicle_track_distance: Optional[Length]
    two_wheeler_track_distance: Optional[Length]
    pedestrian_track_distance: Optional[Length]
    other_access_means: Optional[str]


class ServicesAndEnvironment(AnnexeModel):
    is_school_flood_prone: Optional[bool]
    is_locality_electrified: Optional[list[SourceElectricity]]
    water_supply: Optional[list[SourceEau]]
    is_school_environment_polluted: Optional[list[TypePollution]]


class NearbyEstablishments(AnnexeModel):
    distance_to_preschool: Optional[Distance]
    distance_to_first_primary_school: Optional[Distance]
    distance_to_second_primary_school: Optional[Distance]
    distance_to_secondary_school: Optional[Distance]


class SocioEnvironnement(AnnexeModel):
    """Se réfère à la section Environnement socio économique de l'école"""
    distances: SchoolDistance
    accessibility: SchoolAccessibility
    services_and_environment: ServicesAndEnvironment
    nearby_establishments: NearbyEstablishments
