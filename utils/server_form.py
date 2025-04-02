from django import forms

class FieldHandler:
    def handle(self, field: forms.Field, initial=None):
        raise NotImplementedError("Handle method must be implemented")

class TextFieldHandler(FieldHandler):
    def handle(self, field: forms.CharField, initial=None):
        return {
            "atts": {
                "max_length": field.max_length,
                "min_length": field.min_length,
            },
            "type": "password" if isinstance(field.widget, forms.PasswordInput) else (
                "textarea" if isinstance(field.widget, forms.Textarea) else "text"
            ),
            "label": field.label,
            "required": field.required,
            "initial": initial,
        }

class NumberFieldHandler(FieldHandler):
    def handle(self, field: forms.IntegerField, initial=None):
        return {
            "atts": {
                "max_value": field.max_value,
                "min_value": field.min_value,
            },
            "type": "number",
            "label": field.label,
            "required": field.required,
            "initial": initial,
        }

class ChoiceFieldHandler(FieldHandler):
    def handle(self, field: forms.ChoiceField, initial=None):
        return {
            "atts": {
                "choices": list(field.choices),
            },
            "type": "select",
            "label": field.label,
            "required": field.required,
            "initial": initial,
        }

class TimeFieldHandler(FieldHandler):
    def handle(self, field: forms.TimeField, initial=None):
        return {
            "type": "time",
            "label": field.label,
            "required": field.required,
            "initial": initial,
        }

class DateFieldHandler(FieldHandler):
    def handle(self, field: forms.DateField, initial=None):
        return {
            "type": "date",
            "label": field.label,
            "required": field.required,
            "initial": initial,
        }

class FileFieldHandler(FieldHandler):
    def handle(self, field: forms.FileField, initial=None):
        return {
            "type": "image" if isinstance(field, forms.ImageField) else "file",
            "label": field.label,
            "required": field.required,
            "initial": initial,
        }

class EmailFieldHandler(FieldHandler):
    def handle(self, field: forms.EmailField, initial=None):
        return {
            "type": "email",
            "label": field.label,
            "required": field.required,
            "max_length": field.max_length,
            "min_length": field.min_length,
            "initial": initial,
        }

class BooleanFieldHandler(FieldHandler):
    def handle(self, field: forms.BooleanField, initial=None):
        return {
            "type": "checkbox",
            "label": field.label,
            "required": field.required,
            "initial": initial,
        }

class ModelChoiceFieldHandler(FieldHandler):
    def handle(self, field: forms.ModelChoiceField, initial=None):
        return {
            "atts": {
                "choices": [
                    (obj.id, str(obj)) for obj in field.queryset
                ],
                "empty_label": field.empty_label,
            },
            "type": "select",
            "label": field.label,
            "required": field.required,
            "initial": initial,
        }
class FormFieldsContext:
    def __init__(self):
        self.handlers = {
            forms.CharField: TextFieldHandler(),
            forms.IntegerField: NumberFieldHandler(),
            forms.ChoiceField: ChoiceFieldHandler(),
            forms.TimeField: TimeFieldHandler(),
            forms.DateField: DateFieldHandler(),
            forms.FileField: FileFieldHandler(),
            forms.EmailField: EmailFieldHandler(),
            forms.BooleanField: BooleanFieldHandler(),
            forms.ModelChoiceField: ModelChoiceFieldHandler(),
        }
    
    def handle_form(self, form: forms.Form):
        form_fields = {}
        for field_name, field in form.fields.items():
            form_fields[field_name] = self.handle_field(field, form.initial.get(field_name))
        return form_fields
    

    def handle_field(self, field: forms.Field, initial=None):
        handler = self.handlers.get(type(field), FieldHandler())
        field_dict = handler.handle(field, initial)        
        return field_dict
