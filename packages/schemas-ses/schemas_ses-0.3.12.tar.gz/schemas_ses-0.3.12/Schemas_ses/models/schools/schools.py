from fastapi import HTTPException
from pydantic_core import ValidationError
from pymongo.database import Database
from pymongo.results import UpdateResult
from starlette import status
from typing import get_type_hints

from Schemas_ses.models.model import Model
from Schemas_ses.models.objectid import PydanticObjectId
from Schemas_ses.models.schools.ExamResullt import ExamResult
from Schemas_ses.models.schools.FinancialData import FinancialData
from Schemas_ses.models.schools.GeneralInfo import GeneralInfo
from Schemas_ses.models.schools.IdAndLocation import IdAndLocation
from Schemas_ses.models.schools.OfficeAndFurniture import OfficeAndFurniture
from Schemas_ses.models.schools.ParticipatorySchoolManagement import ParticipatorySchoolManagement
from Schemas_ses.models.schools.SocioEnvironnement import SocioEnvironnement
from Schemas_ses.models.schools.StudentsRecord import StudentsRecord
from Schemas_ses.models.schools.TeachingAndLearningEquipment import TeachingAndLearningEquipment
from Schemas_ses.models.schools.TeachingStaff import TeachingStaff


class Schools(Model):
    name: str
    school_id: str
    id_and_location: IdAndLocation
    socio_environnement: SocioEnvironnement
    general_info: GeneralInfo
    office_and_furniture: OfficeAndFurniture
    teaching_and_learning_equipment: TeachingAndLearningEquipment
    teaching_staff: TeachingStaff
    exam_results: ExamResult
    participatory_school_management: ParticipatorySchoolManagement
    financial_data: FinancialData
    students_record: StudentsRecord

    @classmethod
    def find_one(cls, database: Database, mask: dict):
        if result := database.Schools.find_one(mask):
            # Exclude _id from the result

            return Schools(**result)
        else:
            return None

    @classmethod
    def find_one_or_404(cls, database: Database, mask: dict):
        if result := database.Schools.find_one(mask):
            # Exclude _id from the result

            return Schools(**result)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Utilisateur non trouvé",
            )

    def save(self):
        data = self.to_bson()
        result = self.database.Schools.insert_one(data)
        self.id = PydanticObjectId(result.inserted_id)

    def full_update(self, data: dict):
        self.database.Schools.update_one({"_id": self.id},
                                         {"$set": data})
        self.__init__(**Schools.find_one_or_404(self.database, {"_id": self.id}).dict())

    def partial_update(self, data: dict, section: str) -> UpdateResult:
        try:
            section_model = get_type_hints(Schools)
            validator = section_model[section]
            validator(**data)
            result = self.database.Schools.update_one({"_id": self.id},
                                                      {"$set": {section: data}})
            self.__init__(**Schools.find_one_or_404(self.database, {"_id": self.id}).dict())
            return result
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=e.errors()
            )

