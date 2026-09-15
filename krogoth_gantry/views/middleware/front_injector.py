from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from krogoth_gantry.models.gantry_models import KrogothGantrySlaveViewController, KrogothGantryMasterViewController
from krogoth_gantry.krogoth_compiler import MasterCompiler
from krogoth_gantry.krogoth_static_frontend import render_view_html


class DynamicJavaScriptInjector(APIView):
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        name = request.GET['name']

        if 'lazy' in request.GET:
            lazy_token = request.GET['lazy']
            raw_js = MasterCompiler(username=request.user.username)
            js_response = raw_js.compiled_raw(named=[name, lazy_token]).replace("_LAZY_TOKEN_", lazy_token)
        else:
            raw_js = MasterCompiler(username=request.user.username)
            js_response = raw_js.compiled_raw(named=name)
        return HttpResponse(js_response, content_type='application/javascript; charset=utf-8')


class DynamicHTMLInjector(APIView):
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        name = request.GET['name']
        application = KrogothGantryMasterViewController.objects.get(name=name)
        raw_html_response = render_view_html(application.view_html, application.style_css,
                                             application.get_theme_style)
        return HttpResponse(raw_html_response, content_type='text/html; charset=utf-8')


class DynamicHTMLSlaveInjector(APIView):
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        name = request.GET['name']
        application = KrogothGantrySlaveViewController.objects.get(name=name)
        master = application.owner.get()
        raw_html_response = render_view_html(application.view_html, master.style_css,
                                             master.get_theme_style)
        return HttpResponse(raw_html_response, content_type='text/html; charset=utf-8')

