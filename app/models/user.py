from pydantic import BaseModel,ConfigDict
from typing import Optional
from  bson import ObjectId

class LoginPayload(BaseModel):
    name:str
    password:str
    
class User(BaseModel):
    _id: Optional[ObjectId] = None
    name:str
    password:str

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )

class UserView(BaseModel):
     _id: Optional[ObjectId] = None
     name:str
     
class UserDbModel(UserView):
    def model_dump(self, *, mode = 'python', include = None, exclude = None, context = None, by_alias = None, exclude_unset = False, exclude_defaults = False, exclude_none = False, exclude_computed_fields = False, round_trip = False, warnings = True, fallback = None, serialize_as_any = False, polymorphic_serialization = None):
        data = super().model_dump(mode=mode, include=include, exclude=exclude, context=context, by_alias=by_alias, exclude_unset=exclude_unset, exclude_defaults=exclude_defaults, exclude_none=exclude_none, exclude_computed_fields=exclude_computed_fields, round_trip=round_trip, warnings=warnings, fallback=fallback, serialize_as_any=serialize_as_any, polymorphic_serialization=polymorphic_serialization)

        if self._id:
                data['_id'] = str(data['_id'])

        return data
    
