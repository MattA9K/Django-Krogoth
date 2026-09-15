import os

from krogoth_gantry.models import IncludedHtmlCoreTemplate
from krogoth_gantry.models.gantry_models import KrogothGantryMasterViewController
from krogoth_gantry.models.core_models import AKBowerComponent

from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser
from krogoth_gantry.models.core_models import AKFoundationAbstract
from krogoth_gantry.functions.akfoundation import AKFoundationSerializer
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.viewsets import ModelViewSet
from django.template import loader
from django.http import HttpResponse
from jawn.settings import STATIC_KROGOTH_MODE, BASE_DIR  # , APP_VERSION
from krogoth_gantry.krogoth_static_frontend import frontend_urls
from django.template import Context, Template

# from krogoth_gantry.views.middleware.dj_tmpl_rendered import load_custom_css, load_krogoth_css, load_background_css, \
#     load_core_css, load_core_elements_css

import inspect
from krogoth_gantry.models.krogoth_manager import DataVisitorTracking, DataVisitorMeta, DataServerEvents


class AKFoundationViewSet(ModelViewSet):
    # permission_classes = [IsAdminUser]
    queryset = AKFoundationAbstract.objects.all().order_by('last_name')
    serializer_class = AKFoundationSerializer
    permission_classes = (AllowAny,)
    filter_backends = [DjangoFilterBackend]
    filter_fields = ('unique_name', 'first_name', 'last_name', 'ext',)


# * * * * *
# Any new global CSS customizations should be added here.
# Edit the CSS document at:
# static/web/core/html/layouts/CSS_CustomGlobals.html

def load_custom_css():
    css = IncludedHtmlCoreTemplate.objects.get(name="CSS_CustomGlobals.html")
    template = Template(css.contents)
    context = Context({"foo1": "bar1"})
    rendered = template.render(context)
    return rendered


# * * * * *
# non-Google CSS stylesheets:

def load_krogoth_css():
    css = IncludedHtmlCoreTemplate.objects.get(name="CSS_Krogoth.html")
    template = Template(css.contents)
    context = Context({"foo1": "bar1"})
    rendered = template.render(context)
    return rendered


def load_background_css():
    css = IncludedHtmlCoreTemplate.objects.get(name="CSS_Background.html")
    template = Template(css.contents)
    context = Context({"foo1": "bar1"})
    rendered = template.render(context)
    return rendered


# * * * * *
# core and core elements are the default AngularJS styles from Google:

def load_core_css():
    css = IncludedHtmlCoreTemplate.objects.get(name="CSS_Core.html")
    template = Template(css.contents)
    context = Context({"foo1": "bar1"})
    rendered = template.render(context)
    return rendered


def load_core_elements_css():
    css = IncludedHtmlCoreTemplate.objects.get(name="CSS_CoreElements.html")
    template = Template(css.contents)
    context = Context({"foo1": "bar1"})
    rendered = template.render(context)
    return rendered


def index(request):
    print("🍎 🍎 🍎 🍎 🍎 🍎 🍎 🍎 🍎")
    permission_classes = (AllowAny,)
    
    template = loader.get_template('index_alt.html')
    # template = loader.get_template('coming_soon.html')
    
    splash_title = 'MattA9K'
    font_size = 36
    splash_logo_bg_color = 'antiquewhite'
    width = 250
    main_bg_color = 'darkolive'
    font_color = 'black'

    try:
        usr = 'ANONYMOUS'
        if request.user: usr = request.user.username
        count_this = DataVisitorTracking()
        try: 
            count_this.remote_addr = request.META['REMOTE_ADDR']
            if "67.165.25.161" == str(count_this.remote_addr):
                template = loader.get_template('index_alt.html')
            else:
                template = loader.get_template('index_alt.html')
            print("🫐 🫐 🫐 🫐 🫐" + str(count_this.remote_addr) + "🫐 🫐 🫐 🫐 🫐 ")
        except: 
            pass  # no value for key=[QUERY_STRING]
        try: count_this.remote_port = request.META['REMOTE_PORT']
        except: pass  # no value for key=[QUERY_STRING]
        try: count_this.http_user_agent = request.META['HTTP_USER_AGENT']
        except: pass  # no value for key=[QUERY_STRING]
        try: count_this.username=usr
        except: pass  # no value for key=[QUERY_STRING]



        meta_val = DataVisitorMeta(tracker=count_this)
        try: meta_val.query_string = request.META['QUERY_STRING']
        except: pass
        try: meta_val.content_length = request.META['CONTENT_LENGTH']
        except: pass  # no value for key=[CONTENT_LENGTH]
        try: meta_val.content_type = request.META['CONTENT_TYPE']
        except: pass  # no value for key=[CONTENT_TYPE]
        try: meta_val.http_accept = request.META['HTTP_ACCEPT']
        except: pass  # no value for key=[HTTP_ACCEPT]
        try: meta_val.http_accept_encoding = request.META['HTTP_ACCEPT_ENCODING']
        except: pass  # no value for key=[HTTP_ACCEPT_ENCODING]
        try: meta_val.http_accept_language = request.META['HTTP_ACCEPT_LANGUAGE']
        except: pass  # no value for key=[HTTP_ACCEPT_LANGUAGE]
        try: meta_val.http_host = request.META['HTTP_HOST']
        except: pass  # no value for key=[HTTP_HOST]
        try: meta_val.http_referer = request.META['HTTP_REFERER']
        except: pass  # no value for key=[HTTP_REFERER]
        try: meta_val.remote_host = request.META['REMOTE_HOST']
        except: pass  # no value for key=[REMOTE_HOST]
        try: meta_val.remote_user = request.META['REMOTE_USER']
        except: pass  # no value for key=[REMOTE_USER]
        try: meta_val.request_method = request.META['REQUEST_METHOD']
        except: pass  # no value for key=[REQUEST_METHOD]
        try: meta_val.server_name = request.META['SERVER_NAME']
        except: pass  # no value for key=[SERVER_NAME]
        try: meta_val.server_port = request.META['SERVER_PORT']
        except: pass  # no value for key=[SERVER_PORT]
        count_this.save()
        meta_val.save()
    except Exception as e:
        # print('\n\n\nFAILED TO TRACE\n\n\n')
        DataServerEvents.warn("FAILED TO TRACE " + e.__str__(),
                              inspect.getframeinfo(inspect.stack()[1][0]))

    KrogothGantryMasterViewControllers = []
    all_applications = KrogothGantryMasterViewController.objects.filter(is_enabled=True)
    if STATIC_KROGOTH_MODE == False:
        for application in all_applications:
            KrogothGantryMasterViewControllers.append(
                '/krogoth_gantry/DynamicJavaScriptInjector/?name=' + application.name)
    else:
        # Named per enabled MVC rather than listdir so a stale or missing
        # static/compiled/ cannot inject dead <script> tags or 500 the page.
        for application in all_applications:
            compiled = os.path.join(BASE_DIR, 'static', 'compiled', application.name + '.js')
            if os.path.isfile(compiled):
                KrogothGantryMasterViewControllers.append('/static/compiled/' + application.name + '.js')
            else:
                DataServerEvents.warn(
                    'STATIC_KROGOTH_MODE is on but static/compiled/%s.js is missing. '
                    'Run ./manage.py compilekrogoth' % application.name,
                    inspect.getframeinfo(inspect.stack()[0][0]))
    version_build = 'Krogoth v1.0.02'
    seo_title = "Krogoth "
    seo_description = 'description'
    seo_description += ', description - 2'
    KrogothMainComponents = []
    all_parts = AKFoundationAbstract.objects.filter(is_selected_theme=True)
    for p in all_parts:
        if p.first_name == "core" or \
                p.first_name == "index" or \
                p.first_name == "main" or \
                p.first_name == "quick-panel" or \
                p.first_name == "toolbar" or \
                p.first_name == "navigation":
            pass
        else:
            KrogothMainComponents.append(p.unique_name)
    all_bowers = AKBowerComponent.objects.all()
    context = {
        "version_build": version_build,
        "all_bowers": all_bowers,
        "core": KrogothMainComponents,
        "message": seo_title,
        "description": seo_description,
        "KrogothGantryMasterViewControllers": KrogothGantryMasterViewControllers,
        "splash_title": splash_title,
        "font_size": font_size,
        "splash_logo_bg_color": splash_logo_bg_color,
        "width": width,
        "main_bg_color": main_bg_color,
        "font_color": font_color,
    }
    context.update(frontend_urls(STATIC_KROGOTH_MODE))
    return HttpResponse(template.render(context, request))
