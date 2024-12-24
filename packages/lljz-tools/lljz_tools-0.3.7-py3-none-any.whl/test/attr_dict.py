from os import name
from typing import Any, TypeGuard, TypedDict
from lljz_tools.attribute_dict.pydantic_model import NullableBaseModel
from pydantic import BaseModel

class User(BaseModel):
    
    name: str 
    age: int 
    
    
user = User(name='abc')
print(user.name)