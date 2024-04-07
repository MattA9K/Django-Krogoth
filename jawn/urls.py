from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from krogoth_gantry.views.views_chat import UserViewSet, JawnUserViewSet
from krogoth_gantry.views.index_and_akfoundation import index
from krogoth_gantry.krogoth_modelview_pods import kg_pubstatic_interface
from django.conf.urls.static import static
from jawn import settings_staging

router = DefaultRouter()
router.register(r'users', UserViewSet, 'User')
router.register(r'jawn-users', JawnUserViewSet, 'Jawn User')






urlpatterns = [
    path('kapp_notes/', include('kapp_notes.urls')),
    # Example Stuff
    path('krogoth_examples/', include('krogoth_gantry.routes.urls_krogoth_examples')),
    # path('generic/', include('krogoth_gantry.routes.urls_krogoth_examples')),
    # path('krogoth_dashboard/', include('krogoth_gantry.routes.urls_forums')),

    url(r'^$', index),
    path('admin_a9k/', admin.site.urls),

    path('global_static_interface/', include('krogoth_gantry.krogoth_modelview_pods.kg_pubstatic_interface')),
    path('global_static_text/', include('krogoth_gantry.krogoth_modelview_pods.kg_publicstatic_text')),
    path('moho_extractor/', include('krogoth_gantry.routes.urls_mohoextractor')),
    path('krogoth_gantry/', include('krogoth_gantry.routes.urls_krogoth_gantry')),



    
    # user auth, forgot_password, reset pass, etc..
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('accounts/', include('allauth.urls')),
]


if settings_staging.DEBUG:
    urlpatterns += static(settings_staging.MEDIA_URL, document_root=settings_staging.MEDIA_ROOT)