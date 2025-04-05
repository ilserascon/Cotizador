# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.views.decorators.csrf import csrf_exempt
from .forms import SignUpForm
from utils.server_form import FormFieldsContext
from django.http import JsonResponse, HttpResponseNotAllowed, QueryDict, multipartparser
from django.middleware.csrf import get_token
from .decorators import admin_required
from .models import AppUser
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .validators.user import UserUpdate
from pydantic import ValidationError

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            
            print(f"Usuario: {username}\t| Contraseña: {password}")
            
            user = authenticate(username=username, password=password)
            if user is not None:
                print(f"User: {user}")
                login(request, user)
                return redirect("/")
            else:
                msg = 'Credenciales Inválidas'
        else:
            msg = 'Error de Validación'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


translated_messages = {
    "required": "El campo es requerido",
    "invalid": "El campo no se encuentra en el formato correcto",
    "unique": "Un usuario con estos datos ya existe",
    "max_length": "El campo no puede tener mas de {} caracteres",
    "min_length": "El campo no puede tener menos de {} caracteres",
    "min_value": "El campo no puede ser menor a {}",
    "max_value": "El campo no puede ser mayor a {}",
    "password_too_short": "La contraseña debe tener al menos 8 caracteres"
}

formatted_messages = ['max_length', 'min_length', 'min_value', 'max_value']


@csrf_exempt
@admin_required
def create_user(request):
    formHandler = FormFieldsContext()

    match(request.method):
        case 'GET':
            
            
            form = SignUpForm()
            
            form_json = formHandler.handle_form(form)
            token = get_token(request)
            
            return JsonResponse({"form": form_json, "token": token}, status=200)
    
        case 'POST':
            form = SignUpForm(request.POST)
            token = get_token(request)
            
            if form.is_valid():

                AppUser.objects.create_user(
                    first_name=form.cleaned_data['first_name'], 
                    last_name=form.cleaned_data['last_name'], 
                    email=form.cleaned_data['email'], 
                    role=form.cleaned_data['role'], 
                    username=form.cleaned_data['username'], 
                    password=form.cleaned_data['password1'], 
                    created_by=request.user, 
                    updated_by=request.user
                )
                
                return JsonResponse({"status": "success", "message": "Usuario creado correctamente"})
            else:
                for field, errors in form.errors.items():
                    
                    try:
                        
                        new_message = translated_messages[errors.as_data()[0].code]
                        
                        if errors.as_data()[0].code in formatted_messages:
                            new_message = new_message.format(errors.as_data()[0].params['max_length'])

                        
                        form.errors[field] = [new_message] if new_message else errors
                        
                        
                    except:
                        pass
                    
                return JsonResponse({"status": "error", "data": form.errors}, status=403)
            
            
        
        case _:
            return HttpResponseNotAllowed(['GET', 'POST'])



@csrf_exempt
@admin_required
def edit_user(request, id: int):
    if not request.method in ['GET', 'PUT']:
        return HttpResponseNotAllowed(['GET','PUT'])

    try:
        user = AppUser.undeleted_objects.get(pk=id)
    except AppUser.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Usuario no encontrado"}, status=404)
    
    if request.method == 'GET':
        form = SignUpForm(instance=user)
        form_json = FormFieldsContext().handle_form(form)
        token = get_token(request)
        
        return JsonResponse({"form": form_json, "token": token}, status=200)
    parser = multipartparser.MultiPartParser(request.META, request, request.upload_handlers)

    data, files = parser.parse()

    
    updated_fields = {}
    
    for field in AppUser.updatable_atts:
        if (field in data) and (field != None) and (field != '') and (getattr(user, field) != data[field]):
            updated_fields[field] = data[field]
    
    try:
        updated_relations = {}
        for field in AppUser.updatable_relations:
            if (field in data) and (data[field] != None) and (data[field] != '') and (getattr(user, f'{field}_id') != data[field]):
                updated_relations[field] = data[field]
                
        user_update = UserUpdate(**updated_fields, **updated_relations)
        
        for field, value in user_update:
            if value == None:
                continue
            setattr(user, field, value)
            
        user.updated_by = request.user
        user.save()
        
        return JsonResponse({"status": "success", "title": "Éxito", "message": "Usuario actualizado correctamente", "updated_fields": updated_fields}, status=200)
    
    except ValidationError as err:
        
        # print(err.json())

        error_dict = {}
        print(err.errors())
        print(err)
        
        custom_errors = {
            'value is not a valid email address: An email address must have an @-sign.': 'El correo debe de tener un "@"',
            'value is not a valid email address: There must be something after the @-sign.': 'El correo debe de tener algo despues del "@"',
            'value is not a valid email address: The part after the @-sign is not valid. It should have a period.': 'El correo debe de tener un "." despues del "@"',
            'value is not a valid email address: An email address cannot end with a period.': 'El correo no puede terminar con un "."'
            
        }
        
        for error in err.errors():
            msg = error['msg']
            error_dict[error['loc'][0]] = [custom_errors[msg]] if msg in custom_errors else [msg]
            print(error)

        custom_errors = {
           "string_too_short": "El campo no puede tener menos de {min_length} caracteres",
           "string_too_long": "El campo no puede tener mas de {max_length} caracteres"
        }

        for error in err.errors():
            msg = custom_errors.get(error['type'])
            ctx = error.get('ctx')
            print(f'Message: {msg} | Context: {ctx} | Error: {error}')
            
            if msg:
                error_dict[error['loc'][0]] = [msg.format(**ctx) if ctx else msg]
        
        print(error_dict)
        
        return JsonResponse({"status": "error", "data": error_dict}, status=400)    
    except Exception as err:
        print(err)
        return JsonResponse({"status": "error"}, status=500)
        
    
@csrf_exempt
@admin_required
def get_users(request):
    
    match(request.method):
        case 'GET':
            users = AppUser.undeleted_objects.all().order_by('created_at')
            # --- Search ---
            search_term = request.GET.get('search', None)
            print(search_term)
            if search_term:
                users = users.filter(username=search_term)

            # --- Filtering ---
            for field_name in AppUser.public_atts:
                filter_value = request.GET.get(field_name)
                if filter_value:
                    users = users.filter(**{field_name: filter_value})

            # --- Pagination ---
            page = request.GET.get('page', 1)
            page_size = request.GET.get('page_size', 10)  
            paginator = Paginator(users, page_size)

            try:
                users_page = paginator.page(page)
            except PageNotAnInteger:
                users_page = paginator.page(1)
            except EmptyPage:
                users_page = paginator.page(paginator.num_pages)

            users_data = [user.get_pub_dict() for user in users_page]
            fields_mapping = {AppUser.public_atts[i]: AppUser.displayname_mapping[i] for i in range(len(AppUser.public_atts))}
            
            response_data = {
                "status": "success",
                "data": users_data,
                "headers": fields_mapping,
                "pagination": {
                    "count": paginator.count,
                    "num_pages": paginator.num_pages,
                    "current_page": users_page.number,
                    "has_next": users_page.has_next(),
                    "has_previous": users_page.has_previous(),
                    "next_page_number": users_page.next_page_number() if users_page.has_next() else None,
                    "previous_page_number": users_page.previous_page_number() if users_page.has_previous() else None,
                }
            }
            
            return JsonResponse(response_data, status=200)
            
        case _:
            return HttpResponseNotAllowed(['GET'])

@csrf_exempt
@admin_required
def delete_user(request, id: int):
    if not request.method == 'DELETE':
        return HttpResponseNotAllowed(['DELETE'])
    
    user = AppUser.undeleted_objects.get(pk=id)

    if not user:
        return JsonResponse({"status": "error", "message": "Usuario no encontrado"}, status=404)

    try:
        user.soft_delete()
    except Exception as err:
        print(err)
        return JsonResponse({"status":"error", "message": "No se pudo eliminar el usuario"}, status=500)
    
    return JsonResponse({"status": "success", "message": "Usuario eliminado correctamente"})
    