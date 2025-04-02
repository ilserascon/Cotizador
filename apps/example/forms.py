from django import forms
from utils.validation_messages import ValidationMessages
from .models import Person


class PersonCreationForm(forms.Form):
  first_name = forms.CharField(
    label="Nombre",
    max_length=50,
    min_length=5,
  )
  last_name = forms.CharField(
    label="Apellido",
    max_length=60,
    min_length=5,
  )
  age=forms.IntegerField(
    label="Edad",
    max_value=125,
    min_value=18,
  )
  companie=forms.ChoiceField(choices=[('Ford','Ford'), ('DHL','DHL'), ('Toyota','Toyota')], initial='Ford', label="Compañía")
  hire_date=forms.TimeField(required=True, label="Fecha de contratación")
  comments=forms.CharField(
    widget=forms.Textarea(),
    label="Comentarios",
    max_length=256,
    min_length=10,
    required=False,
  )

class PersonModelForm(forms.ModelForm):
  class Meta:
    model = Person
    fields = ['first_name', 'last_name', 'age']
    labels = {
      "first_name" : "Nombre",
      "last_name" : "Apellido",
      "age" : "Edad",
    }
    
  

ValidationMessages.change_form_error_messages(PersonCreationForm)
