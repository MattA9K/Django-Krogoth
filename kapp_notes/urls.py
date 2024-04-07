from kapp_notes.views import AKNoteViewSet
from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter



router_notes = DefaultRouter()
router_notes.register(r'note', AKNoteViewSet, 'AKNoteViewSet')

urlpatterns = [
    path('', include(router_notes.urls)),
]

