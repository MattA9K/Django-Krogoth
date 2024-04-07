from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from kapp_notes.models import AKNote
from kapp_notes.serializers import AKNoteSerializer



class AKNoteViewSet(viewsets.ModelViewSet):
    queryset = AKNote.objects.all()
    serializer_class = AKNoteSerializer
    permission_classes = (IsAuthenticated,)


