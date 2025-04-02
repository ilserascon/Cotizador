from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import  HttpResponse
from django import template
from django.urls import get_resolver


@login_required(login_url="/auth/login/")
def index(request):

    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/auth/login/")
def pages(request):    

    context = {'segment': request.path.split('/')[-1]}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
            
    try:

        load_template = 'home/'+ request.path.split('home/')[-1]
        html_template = loader.get_template(load_template)
        
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request), status=404)

    except:
        html_template = loader.get_template('home/page-500.html', status=500)
        return HttpResponse(html_template.render(context, request))
