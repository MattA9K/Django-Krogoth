from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from krogoth_gantry.models.forum_models import AKThread, AKThreadCategory, AKThreadSocialMedia, ForumThreadCategory, ForumThreadOP, \
    ForumThreadReply
from krogoth_gantry.functions.forum_apis import AKThreadSerializer, AKThreadSocialMediaSerializer, \
    AKThreadReplySocialMediaSerializer, AKThreadCategorySerializer, ForumThreadOPSerializer, ForumThreadReplySerializer, \
    ForumThreadCategorySerializer
from rest_framework.views import APIView
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from krogoth_gantry.models.models_chat import JawnUser
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
import random


class ForumThreadCategoryViewSet(viewsets.ModelViewSet):
    queryset = ForumThreadCategory.objects.all()
    serializer_class = ForumThreadCategorySerializer
    permission_classes = (IsAuthenticated,)


class ForumThreadOPViewSet(viewsets.ModelViewSet):
    queryset = ForumThreadOP.objects.all()
    serializer_class = ForumThreadOPSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filter_fields = ('author', 'category',)


class ForumThreadReplyViewSet(viewsets.ModelViewSet):
    queryset = ForumThreadReply.objects.all()
    serializer_class = ForumThreadReplySerializer
    permission_classes = (IsAuthenticated,)
    # filter_backends = [DjangoFilterBackend]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['author', 'parent',]
    # filter_fields = ('author', 'parent',)


class AKThreadCategoryViewSet(viewsets.ModelViewSet):
    queryset = AKThreadCategory.objects.all()
    serializer_class = AKThreadCategorySerializer
    permission_classes = (AllowAny,)
    filter_backends = [DjangoFilterBackend]
    filter_fields = ('uid',)
    

class AKThreadViewSet(viewsets.ModelViewSet):
     queryset = AKThread.objects.all()
     serializer_class = AKThreadSerializer
     permission_classes = (AllowAny,)
     filter_backends = [DjangoFilterBackend]
     filter_fields = ('author', 'parent', 'category',)


class AKThreadListView(generics.ListAPIView):
    queryset = AKThread.objects.all()
    serializer_class = AKThreadSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('date_modified', )
    ordering = ('date_modified',)


class AKThreadSocialMediaViewSet(viewsets.ModelViewSet):
    queryset = AKThreadSocialMedia.objects.filter(parent=None)
    serializer_class = AKThreadSocialMediaSerializer
    permission_classes = (AllowAny,)
    filter_backends = [DjangoFilterBackend]
    filter_fields = ('author', 'parent', 'category',)

class AKThreadSocialMediaReplyViewSet(viewsets.ModelViewSet):
    queryset = AKThreadSocialMedia.objects.filter(title="REPLY")
    serializer_class = AKThreadReplySocialMediaSerializer
    permission_classes = (AllowAny,)
    filter_backends = [DjangoFilterBackend]
    filter_fields = ('author', 'parent', 'category',)


class update_thread_moddate(APIView):
    #authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    def get(self, request, format=None):
        thread = request.GET['threadId']         
        op = AKThread.objects.get(uid=thread)
        op.date_modified = datetime.now()
        op.save(update_fields=["date_modified"]) 
        return HttpResponse("ITS GOOD", content_type='text/html; charset=utf-8')
        
        
class manual_post_method(APIView):
    #authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    def post(self, request, format=None):
        print("\n\n")
        print(request.POST)
        print("..........\n")
        thread = request.POST['threadId']         
        return HttpResponse("ITS GOOD " + thread, content_type='text/html; charset=utf-8')
  
  
class manual_post_reply(generics.CreateAPIView):
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        print("\n\n")
        print(request.data)
        print("..........\n")
        
        
        _title = "REPLY"
        _pub_date = datetime.now()
        _date_modified = datetime.now()
        _is_deleted = False
        _parent = request.data['parent']
        _content = request.data['content']
        _type = request.data['type']
        _text_body = "not implemented"
        _likes = 0
        _p = AKThread.objects.get(uid=_parent)
        children = AKThread.objects.filter(parent=_parent)
        _p.date_modified = datetime.now()
        _p.save()

        _author = JawnUser.objects.get(base_user=request.user)
        _r = AKThreadSocialMedia.objects.create(title=_title, author=_author, pub_date=_pub_date, date_modified=_date_modified,
                      is_deleted=_is_deleted, parent=_p, content=_content, type=_type, likes=0, text_body=_text_body, uid=str(random.randint(0,999999)))
        _r.save()
        return JsonResponse("ITS GOOD " , content_type='application/json; charset=utf-8', safe=False)