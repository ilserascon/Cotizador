from pydantic import BaseModel, ValidationError, PlainValidator, EmailStr, Field
from apps.authentication.models import UserRole, AppUser
from typing import Annotated, Any, Optional
from apps.authentication.constants import (
  USERNAME_MAX_LENGTH,
  USERNAME_MIN_LENGTH,
  FIRST_NAME_MAX_LENGTH,
  FIRST_NAME_MIN_LENGTH,
  LAST_NAME_MAX_LENGTH,
  LAST_NAME_MIN_LENGTH,
  EMAIL_MAX_LENGTH,
  EMAIL_MIN_LENGTH,
  PASSWORD_MAX_LENGTH,
  PASSWORD_MIN_LENGTH
)


def valid_role(identifier: Any) -> Any:
  if isinstance(identifier, str):
    try:
      identifier = int(identifier)

      role = UserRole.objects.get(pk=identifier)
    
      if not role:
        raise ValidationError('El rol inidicado no existe') 
    
      return role
  
    except:
      pass
    role = UserRole.objects.get(name=identifier)
    
    if not role:
      raise ValidationError('El rol inidicado no existe') 
    
    return role
  
  if isinstance(identifier, int):
      role = UserRole.objects.get(pk=identifier)
    
      if not role:
        raise ValidationError('El rol inidicado no existe') 
    
      return role

  
  raise ValidationError('El rol inidicado no existe')
    

def unique_username(identifier: Any) -> Any:
  if isinstance(identifier, str):
    user = AppUser.objects.filter(username=identifier)

    if user:
      raise ValidationError('El nombre de usuario ya esta en uso')
    
    return identifier
 
  
ValidRole = Annotated[UserRole, PlainValidator(valid_role)]
UniqueUsername = Annotated[str, PlainValidator(unique_username)]


class UserCreation(BaseModel):
  username: UniqueUsername = Field(
    min_length=USERNAME_MIN_LENGTH,
    max_length=USERNAME_MAX_LENGTH,
  )
  first_name: str = Field(
    min_length=USERNAME_MIN_LENGTH,
    max_length=USERNAME_MAX_LENGTH,
  )
  last_name: str = Field(
    min_length=LAST_NAME_MIN_LENGTH,
    max_length=LAST_NAME_MAX_LENGTH, 
  )
  email: EmailStr = Field(
    min_length=EMAIL_MIN_LENGTH,
    max_length=EMAIL_MAX_LENGTH,
  )
  
  role: ValidRole

  password: str = Field(
    min_length=PASSWORD_MIN_LENGTH,
    max_length=PASSWORD_MAX_LENGTH,
  )
  
  

class UserUpdate(BaseModel):
  username: Optional[UniqueUsername] = Field(
    default=None,
    min_length=USERNAME_MIN_LENGTH,
    max_length=USERNAME_MAX_LENGTH,
  )
  first_name: Optional[str] = Field(
    default=None,
    min_length=FIRST_NAME_MIN_LENGTH,
    max_length=FIRST_NAME_MAX_LENGTH,
  )
  last_name: Optional[str] = Field(
    default=None, 
    min_length=LAST_NAME_MIN_LENGTH,
    max_length=LAST_NAME_MAX_LENGTH,
  )
  email: Optional[EmailStr] = Field(
    default=None,
    min_length=EMAIL_MIN_LENGTH,
    max_length=EMAIL_MAX_LENGTH,
  )

  role: Optional[ValidRole] = None

  password: Optional[str] = Field(
    default=None, 
    min_length=PASSWORD_MIN_LENGTH,
    max_length=PASSWORD_MAX_LENGTH,
  )
  
  # @field_validator('email', mode='after')
  # def validate_email(cls, value):
  #     email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
  #     if value and not re.match(email_regex, value):
  #         raise ValidationError('El correo electrónico no es válido')
  #     return value
  
  
  
  
    
  
    
    
    