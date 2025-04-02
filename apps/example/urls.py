from django.urls import path, re_path
from .views  import pages

urlpatterns = [
  path('' , pages.index, name='index'),

  #Match pages
  re_path(r'^.*\.*', pages.pages, name='pages'),    
  
]
