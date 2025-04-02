from django.db import migrations

def create_user_roles(apps, schema_editor):
  UserRole = apps.get_model('authentication', 'UserRole')
  user_roles = ['ADMINISTRADOR', 'USUARIO']

  for user_role in user_roles:
    UserRole.objects.create(name=user_role)
    
def create_users(apps, schema_editor):
  AppUser = apps.get_model('authentication', 'AppUser')
  UserRole = apps.get_model('authentication', 'UserRole')
  
  admin_role = UserRole.objects.get(name='ADMINISTRADOR')
  user_role = UserRole.objects.get(name='USUARIO')
  
  
  if not AppUser.objects.filter(username='admin').exists():
    admin = AppUser.objects.create_user(
      username='admin',
      password='admin',
      role=admin_role,
    )
    admin.save()
  if not AppUser.objects.filter(username='user').exists():
    user = AppUser.objects.create_user(
      username='user',
      password='user',
      role=user_role,
    )
    user.save()
    

class Migration(migrations.Migration):
  dependencies = [
    ('authentication', '0001_initial'),
  ]

  operations = [
    migrations.RunPython(create_user_roles),
    migrations.RunPython(create_users),
  ]