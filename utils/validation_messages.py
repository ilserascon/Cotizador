from django import forms

class ValidationMessages:

  @staticmethod
  def __required():
    return ('required', 'El campo es requerido')
  
  @staticmethod
  def __invalid():
    return ('invalid', 'El campo no se encuentra en el formato correcto')
  
  @staticmethod
  def __unique():
    return ('unique', 'El campo ya existe')

  @staticmethod
  def __max_length(max_length: int):
    return ('max_length', f'El campo no puede tener mas de {max_length} caracteres') 
  
  @staticmethod
  def __min_length(min_length: int):
    return ('min_length', f'El campo no puede tener menos de {min_length} caracteres') 

  @staticmethod
  def __min_value(min_value: int):
    return ('min_value', f'El campo no puede ser menor a {min_value}')

  @staticmethod
  def __max_value(max_value: int):
    return ('max_value', f'El campo no puede ser mayor a {max_value}')
  
  
  @staticmethod
  def get_charfield_messages(max_length=0 , min_length=0, required=False):
    error_messages = {
      "invalid": "El campo no se encuentra en el formato correcto"
    }

    if max_length:
      key, value = ValidationMessages.__max_length(max_length) 
      error_messages[key] = value

    if min_length:
      key, value = ValidationMessages.__min_length(min_length) 
      error_messages[key] = value

    if required:
      key, value = ValidationMessages.__required() 
      error_messages[key] = value

    return error_messages

  @staticmethod
  def get_integerfield_messages(max_value=0 , min_value=0, required=False):
    error_messages = {
      "invalid": "El campo debe de ser un entero"
    }

    if max_value:
      key, value = ValidationMessages.__max_value(max_value) 
      error_messages[key] = value

    if min_value:
      key, value = ValidationMessages.__min_value(min_value) 
      error_messages[key] = value

    if required:
      key, value = ValidationMessages.__required() 
      error_messages[key] = value

    return error_messages
  
  @staticmethod
  def change_form_error_messages(form: forms.Form.__class__):
    for field in form.base_fields.values():
      
      error_messages = field.error_messages
      if isinstance(field, forms.CharField): 
        max_length = int(field.max_length) if field.max_length else 0
        min_length = int(field.min_length) if field.min_length else 0
        error_messages = ValidationMessages.get_charfield_messages(max_length, min_length, field.required)

      elif isinstance(field, forms.IntegerField): 
        max_value = int(field.max_value) if field.max_value else 0
        min_value = int(field.min_value) if field.min_value else 0
        error_messages = ValidationMessages.get_integerfield_messages(max_value, min_value, field.required)

      

      field.error_messages = error_messages



