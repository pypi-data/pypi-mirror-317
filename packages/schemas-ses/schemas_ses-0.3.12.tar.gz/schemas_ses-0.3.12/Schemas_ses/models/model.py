import inspect
from typing import Optional, Any

from pydantic import BaseModel, Field
from datetime import date, datetime

from Schemas_ses.models.objectid import PydanticObjectId


class Model(BaseModel):
    id: Optional[PydanticObjectId] = Field(None, alias="_id")
    database: Optional[Any] = None

    @staticmethod
    def convert_values(obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()  # Convertir les dates en ISO
        elif isinstance(obj, list):
            return [Model.convert_values(item) for item in obj]  # Appliquer la conversion à chaque élément d'une liste
        elif isinstance(obj, dict):
            return {key: Model.convert_values(value) for key, value in
                    obj.items()}  # Appliquer la conversion à chaque élément d'un dictionnaire
        else:
            return obj  # Retourner l'objet inchangé s'il est sérialisable
            # Appliquer la conversion récursive au dictionnaire principal

    def dict(self, *args, **kwargs):
        kwargs["exclude"] = kwargs.get("exclude", set()) | {"database"}
        properties = [prop_name for prop_name, prop in inspect.getmembers(self.__class__) if isinstance(prop, property)]
        for prop in properties:
            getattr(self, prop)
        return Model.convert_values(super().dict(*args, **kwargs))

    def set_db(self, database):
        self.database = database

    def to_bson(self, to_exclude=None):
        if to_exclude is None:
            to_exclude = set()
        to_exclude.add("database")
        data = self.dict(by_alias=True, exclude=to_exclude)
        if "_id" in data and data["_id"] is None:
            data.pop("_id")
        return data


class AnnexeModel(BaseModel):
    ...
