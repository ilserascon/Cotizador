from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.soft_delete import SoftDeleteModel



class UserRole(models.Model):
  name = models.CharField(max_length=50, unique=True)
  
  class Meta:
    db_table = 'user_role'
    verbose_name = 'Role'
    verbose_name_plural = 'Roles'
    
  def __str__(self):
    return f"{self.name}"



class AppUser(AbstractUser, SoftDeleteModel):
  public_atts = ['id','username', 'first_name', 'last_name', 'email', 'role', 'created_at', 'updated_at', 'created_by', 'updated_by']
  displayname_mapping = ['Id','Nombre de usuario', 'Nombre', 'Apellido', 'Correo electrónico', 'Tipo', 'Creado el', 'Actualizado el', 'Creado por', 'Actualizado por']

  role = models.ForeignKey(UserRole, on_delete=models.PROTECT, null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  created_by = models.ForeignKey('self', on_delete=models.PROTECT, related_name='user_created_by', null=True, blank=True)
  updated_by = models.ForeignKey('self', on_delete=models.PROTECT, related_name='user_updated_by', null=True, blank=True)

  def get_pub_dict(self) -> dict:
    return {
      "id": self.id,
      "username": self.username,
      "first_name": self.first_name,
      "last_name": self.last_name,
      "email": self.email,
      "role": self.role.name,
      "created_at": str(self.created_at),
      "updated_at": str(self.updated_at),
      "created_by": self.created_by.username if self.created_by else None,
      "updated_by": self.updated_by.username if self.updated_by else None,
    }
    
  
  class Meta:
    db_table = 'auth_users'
    verbose_name = 'User'
    verbose_name_plural = 'Users'
    
  def __str__(self):
    return f"{self.username}"
  
    